import requests
import json
import time

ETHERSCAN_API_KEY = "YOUR_ETHERSCAN_API_KEY"

def get_erc20_transfers(address):
    url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("result", [])

def detect_dust(transfers, min_threshold_usd=0.5):
    suspicious = []
    for tx in transfers:
        value = int(tx["value"]) / (10 ** int(tx["tokenDecimal"]))
        if value < 1e-4:
            suspicious.append({
                "tokenSymbol": tx["tokenSymbol"],
                "value": value,
                "from": tx["from"],
                "tokenName": tx["tokenName"],
                "hash": tx["hash"]
            })
    return suspicious

def main():
    address = input("Enter Ethereum wallet address: ").strip()
    print("[*] Fetching token transfers...")
    transfers = get_erc20_transfers(address)
    if not transfers:
        print("[-] No token transfers found.")
        return

    print(f"[+] Found {len(transfers)} transfers. Scanning for dust...")
    dust = detect_dust(transfers)
    
    if dust:
        print(f"[!] Suspicious low-value tokens found ({len(dust)}):\n")
        for i, d in enumerate(dust, 1):
            print(f"{i}. {d['tokenSymbol']} ({d['tokenName']}): {d['value']} from {d['from']} [tx: {d['hash'][:12]}...]")
    else:
        print("[✓] No suspicious tokens detected.")

if __name__ == "__main__":
    main()

