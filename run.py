import subprocess
import sys
import pkg_resources
from dotenv import load_dotenv, set_key
import tweepy
import os

# Function to check and install required libraries
def install_requirements():
    required = {'tweepy', 'python-dotenv'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    if missing:
        print("Installing missing libraries...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
    else:
        print("All required libraries are already installed.")

# Install required libraries at the beginning
install_requirements()

# Load environment variables from .env file
def load_or_create_env():
    env_file = '.env'
    if not os.path.exists(env_file):
        print(f"{env_file} file not found. Creating it now...")
        create_env_file()
    load_dotenv()  # Load environment variables from .env file

# Create .env file if it does not exist
def create_env_file():
    # Collect credentials from user
    print("Please enter your Twitter API credentials:")

    TWITTER_API_KEY = input("Enter Twitter API Key: ")
    TWITTER_API_SECRET = input("Enter Twitter API Secret: ")
    TWITTER_ACCESS_TOKEN = input("Enter Twitter Access Token: ")
    TWITTER_ACCESS_TOKEN_SECRET = input("Enter Twitter Access Token Secret: ")

    # Create .env file with the provided credentials
    with open('.env', 'w') as f:
        f.write(f"TWITTER_API_KEY={TWITTER_API_KEY}\n")
        f.write(f"TWITTER_API_SECRET={TWITTER_API_SECRET}\n")
        f.write(f"TWITTER_ACCESS_TOKEN={TWITTER_ACCESS_TOKEN}\n")
        f.write(f"TWITTER_ACCESS_TOKEN_SECRET={TWITTER_ACCESS_TOKEN_SECRET}\n")
    
    print(".env file has been created with your Twitter API credentials.")

# Function to initialize Twitter API client
def initialize_twitter_api():
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
        print("Error: Missing Twitter API credentials.")
        exit(1)

    auth = tweepy.OAuth1UserHandler(
        TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )
    return tweepy.API(auth)

# Search for tweets about Solana meme coins
def search_solana_memecoins(api, query, count=100):
    try:
        print(f"Searching tweets for query: {query}")
        tweets = api.search_tweets(q=query, count=count, lang="en", result_type="mixed")
        return [
            {
                "text": tweet.text,
                "likes": tweet.favorite_count,
                "retweets": tweet.retweet_count,
                "created_at": tweet.created_at,
            }
            for tweet in tweets
        ]
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return []

# Analyze and find popular tweets
def analyze_popular_tweets(tweets):
    sorted_tweets = sorted(tweets, key=lambda x: (x["likes"], x["retweets"]), reverse=True)
    return sorted_tweets[:5]  # Top 5 most popular tweets

# Main function
def main():
    # Load environment variables or create .env if not found
    load_or_create_env()

    # Initialize Twitter API
    twitter_api = initialize_twitter_api()

    # Define search query (keywords related to Solana meme coins)
    query = "solana meme coin OR solana meme crypto OR $SAMO OR Bonk"

    # Fetch tweets
    tweets = search_solana_memecoins(twitter_api, query)

    if tweets:
        print("\nTop Popular Tweets About Solana Meme Coins:")
        for tweet in analyze_popular_tweets(tweets):
            print(f"Tweet: {tweet['text']}")
            print(f"Likes: {tweet['likes']}, Retweets: {tweet['retweets']}, Created At: {tweet['created_at']}\n")
    else:
        print("No tweets found.")

if __name__ == "__main__":
    main()
