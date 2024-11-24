import subprocess
import sys

# Function to install required libraries
def install_requirements():
    try:
        import requests
        import bs4
    except ImportError:
        print("Required libraries are not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4"])

# Function to fetch and parse the webpage
def fetch_wallets(url):
    import requests  # Ensure requests is imported within the function
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Error fetching page:", response.status_code)
        return None

# Function to extract wallet data from the page
def extract_wallet_data(page_content):
    from bs4 import BeautifulSoup  # Ensure BeautifulSoup is imported within the function
    soup = BeautifulSoup(page_content, 'html.parser')

    # Locate the data container for trades or wallets (this may vary based on the actual page structure)
    wallet_data = []

    # Example: Look for divs with specific class names for wallets (change according to actual structure)
    wallet_rows = soup.find_all('div', class_='trade-card')  # Modify as per the correct HTML element

    for row in wallet_rows:
        wallet_info = {}

        # Extract the wallet address (modify based on actual element and class)
        wallet_info['wallet'] = row.find('span', class_='wallet-address').text.strip()

        # Extract the PNL percentage (modify based on actual element and class)
        pnl_text = row.find('span', class_='pnl-value').text.strip()
        try:
            wallet_info['pnl'] = float(pnl_text.replace('%', ''))
        except ValueError:
            wallet_info['pnl'] = None

        if wallet_info['pnl'] is not None and wallet_info['pnl'] > 500:
            wallet_data.append(wallet_info)

    return wallet_data

# Main function
def main():
    # Install the requirements before running the script
    install_requirements()

    url = "https://birdeye.so/find-trades?chain=solana"
    page_content = fetch_wallets(url)
    
    if page_content:
        wallets = extract_wallet_data(page_content)

        if wallets:
            print("Wallets with PNL > $500:")
            for wallet in wallets:
                print(f"Wallet: {wallet['wallet']}, PNL: {wallet['pnl']}$")
        else:
            print("No wallets found with PNL > $500.")
    else:
        print("Failed to fetch or parse the page.")

if __name__ == "__main__":
    main()
