###### No esta funcionando, no se pueden obtener los tweets de Deltaone

import snscrape.modules.twitter as sntwitter
from datetime import timezone

def get_news() -> list[dict]:
    tweets = []
    for tweet in sntwitter.TwitterUserScraper("Deltaone").get_items():
        if tweet.lang == "en":
            tweets.append({
                "source": "Twitter/Deltaone",
                "date": tweet.date.astimezone(timezone.utc).isoformat(),
                "title": tweet.content[:100],
                "description": tweet.content,
                "url": f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
            })
        if len(tweets) >= 10:
            break
    return tweets