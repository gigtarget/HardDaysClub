import feedparser

RSS_FEED_URL = "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"

def fetch_top_news():
    feed = feedparser.parse(RSS_FEED_URL)
    for entry in feed.entries:
        try:
            title = entry.title
            summary = getattr(entry, "summary", getattr(entry, "description", ""))
            return title, summary
        except Exception as e:
            continue
    return None, None
