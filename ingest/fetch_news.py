import asyncpg
from datetime import datetime
import feedparser
import requests
from bs4 import BeautifulSoup

async def insert_news(pool, ts, headline, content, url, sentiment_score=None):
    """
    Insert a news article into the news_raw table.

    Args:
        pool: AsyncPG connection pool
        ts: Timestamp of the news article
        headline: News headline/title
        content: Full text content of the article
        url: URL of the article
        sentiment_score: Optional sentiment score (can be calculated later)
    """
    async with pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO news_raw(ts, headline, content, url, sentiment_score)
            VALUES ($1, $2, $3, $4, $5)
        ''', ts, headline, content, url, sentiment_score)

async def fetch_rss_news(rss_url):
    """
    Fetch news from an RSS feed.

    Args:
        rss_url: URL of the RSS feed

    Returns:
        List of news articles with timestamp, headline, content, and url
    """
    print(f"Fetching from: {rss_url}")
    feed = feedparser.parse(rss_url)
    print(f"Feed status: {feed.get('status', 'unknown')}")
    print(f"Number of entries: {len(feed.entries)}")

    if feed.bozo:
        print(f"Feed parse warning: {feed.bozo_exception}")

    news_items = []

    for entry in feed.entries:
        # Parse timestamp
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            ts = datetime(*entry.published_parsed[:6])
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            ts = datetime(*entry.updated_parsed[:6])
        else:
            ts = datetime.now()

        # Extract headline
        headline = entry.title if hasattr(entry, 'title') else ''

        # Extract content
        content = ''
        if hasattr(entry, 'summary'):
            content = entry.summary
        elif hasattr(entry, 'description'):
            content = entry.description

        # Extract URL
        url = entry.link if hasattr(entry, 'link') else ''

        news_items.append({
            'ts': ts,
            'headline': headline,
            'content': content,
            'url': url
        })

    return news_items

async def main():
    # Create database connection pool
    pool = await asyncpg.create_pool("postgresql://postgres:postgres@localhost:5432/postgres")

    # Working RSS feeds for financial news
    rss_feeds = [
        'https://finance.yahoo.com/news/rssindex',
        'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',  # WSJ Markets
        'https://www.cnbc.com/id/10001147/device/rss/rss.html',  # CNBC Top News
    ]

    # Try each feed until we find one that works
    all_news = []
    for feed_url in rss_feeds:
        try:
            news_items = await fetch_rss_news(feed_url)
            all_news.extend(news_items)
            if news_items:
                break  # Stop after first successful feed
        except Exception as e:
            print(f"Error fetching from {feed_url}: {e}")
            continue

    if not all_news:
        print("No news items fetched from any feed!")
        await pool.close()
        return

    # Insert news items into database
    for item in all_news:
        await insert_news(
            pool,
            item['ts'],
            item['headline'],
            item['content'],
            item['url'],
            None  # sentiment_score can be calculated later
        )
        print(f"Inserted: {item['headline'][:50]}...")

    await pool.close()
    print(f"Successfully inserted {len(all_news)} news articles")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
