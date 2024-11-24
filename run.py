import tweepy
import requests

# Twitter API credentials (replace with your credentials)
TWITTER_API_KEY = 'your_api_key'
TWITTER_API_SECRET = 'your_api_secret'
TWITTER_ACCESS_TOKEN = 'your_access_token'
TWITTER_ACCESS_TOKEN_SECRET = 'your_access_token_secret'

# NewsAPI key (replace with your key)
NEWS_API_KEY = 'your_news_api_key'

# Initialize Twitter API client
def initialize_twitter_api():
    auth = tweepy.OAuth1UserHandler(
        TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )
    return tweepy.API(auth)

# Fetch tweets from a Twitter list
def fetch_tweets_from_list(api, list_id, count=50):
    try:
        tweets = api.list_timeline(list_id=list_id, count=count)
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
        print(f"Error fetching tweets from list: {e}")
        return []

# Search trending news/memes using NewsAPI
def fetch_news_articles(query, page_size=10):
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=popularity&pageSize={page_size}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        print(f"Error fetching news articles: {response.status_code}")
        return []

# Analyze and find the most popular tweets
def analyze_popular_tweets(tweets):
    sorted_tweets = sorted(tweets, key=lambda x: (x["likes"], x["retweets"]), reverse=True)
    return sorted_tweets[:5]

# Main function
def main():
    # Initialize Twitter API
    twitter_api = initialize_twitter_api()

    # Twitter list ID (replace with the actual list ID from the provided link)
    list_id = "1654276583606177793"

    # Fetch tweets from the Twitter list
    print("Fetching tweets from the Twitter list...")
    tweets = fetch_tweets_from_list(twitter_api, list_id)
    print("Top Tweets by Popularity:")
    for tweet in analyze_popular_tweets(tweets):
        print(f"Tweet: {tweet['text']}\nLikes: {tweet['likes']}, Retweets: {tweet['retweets']}\n")

    # Fetch trending news articles about memes
    print("\nFetching trending news articles about memes...")
    news_articles = fetch_news_articles("memes")
    print("Top News Articles:")
    for article in news_articles[:5]:
        print(f"Title: {article['title']}\nSource: {article['source']['name']}\nURL: {article['url']}\n")

if __name__ == "__main__":
    main()
