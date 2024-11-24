import subprocess
import sys
import requests
from bs4 import BeautifulSoup

# Function to install requirements automatically
def install_requirements():
    required_packages = ['requests', 'beautifulsoup4']
    for package in required_packages:
        try:
            # Try to import the package
            __import__(package)
        except ImportError:
            print(f"{package} not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Function to fetch and parse the webpage content using a premium proxy with authentication
def fetch_wallets(url, proxies=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

# Function to extract wallet data from the page
def extract_wallet_data(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')

    # Extract the wallet data (based on the structure of the page, we may need to adjust)
    wallet_data = []

    # Find the wallet rows - Adjust this based on the actual HTML structure
    wallet_rows = soup.find_all('div', class_='trade-card')  # Update with actual class name or identifier

    for row in wallet_rows:
        wallet_info = {}

        # Extract the wallet address
        wallet_address = row.find('span', class_='wallet-address')  # Update this to the correct element
        if wallet_address:
            wallet_info['wallet'] = wallet_address.text.strip()

        # Extract the PNL for the 7d period
        pnl_text = row.find('span', class_='pnl-value')  # Update this to the correct element
        if pnl_text:
            try:
                pnl_value = pnl_text.text.strip().replace('$', '').replace(',', '')  # Remove dollar signs and commas
                pnl_value = float(pnl_value)
                if pnl_value > 700:
                    wallet_info['pnl'] = pnl_value
                    wallet_data.append(wallet_info)
            except ValueError:
                continue

    return wallet_data

# Main function
def main():
    # Install required dependencies
    install_requirements()

    # URL to fetch wallets data from
    url = "https://birdeye.so/find-trades?chain=solana"

    # Premium proxy configuration with authentication
    proxy_user = 'your_proxy_username'
    proxy_pass = 'your_proxy_password'
    proxy_address = 'your_proxy_address'
    proxy_port = 'proxy_port'

    # Set up the proxy URL for HTTP/HTTPS requests
    proxies = {
        'http': f'http://leetsyso:pxevnrkjn3ui@198.23.239.134:6540/',
        'http': f'https://http://leetsyso:pxevnrkjn3ui@198.23.239.134:6540/'
    }
    
    # Fetch the page content with the proxy
    page_content = fetch_wallets(url, proxies=proxies)
    
    if page_content:
        wallets = extract_wallet_data(page_content)

        if wallets:
            print("Wallets with PNL greater than $700 in 7 days:")
            for wallet in wallets:
                print(f"Wallet Address: {wallet['wallet']}, PNL: ${wallet['pnl']}")
        else:
            print("No wallets found with PNL greater than $700 in 7 days.")
    else:
        print("Failed to fetch or parse the page.")

if __name__ == "__main__":
    main()
