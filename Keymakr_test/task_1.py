import aiohttp
import asyncio
import sqlite3
import csv
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

API_URL = "https://jsonplaceholder.typicode.com/posts"
DB_NAME = "posts.sqlite3"
CSV_NAME = "posts.csv"


async def fetch_posts(session: aiohttp.ClientSession, post_id: int) -> None:
    """Асинхронне отримання даних з API"""
    try:
        async with session.get(f"{API_URL}/{post_id}") as response:
            if response.status == 200:
                return await response.json()
            else:
                logging.warning(f"Error fetching post {post_id}: {response.status}")
                return None
    except asyncio.TimeoutError:
        logging.error(f"Timeout fetching post {post_id}")
    except aiohttp.ClitntError:
        logging.error(f"Error fetching post {post_id}")
    return None


async def fetch_all_posts() -> list[dict]:
    """Асинхронне отримання всіх постів"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_posts(session, post_id) for post_id in range(1, 101)]
        return await asyncio.gather(*tasks)


def save_to_db(posts: list[dict]) -> None:
    """Зберігає пости в базу даних sqlite3"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            body TEXT
        )
    """)

    cursor.executemany("""
    INSERT OR REPLACE INTO posts (id, user_id, title, body)
    VALUES (:id, :userId, :title, :body)
    """, posts)

    conn.commit()
    conn.close()
    logging.info("Posts saved to database")


def save_to_csv(posts: list[dict]) -> None:
    """Зберігає дані в CSV форматі"""
    with open(CSV_NAME, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "userId", "title", "body"])
        writer.writeheader()
        writer.writerows(posts)
    logging.info("Posts saved to CSV")


async def main() -> None:
    """Головна функція"""
    logging.info("Starting fetching process")
    posts = await fetch_all_posts()
    posts = [post for post in posts if post]
    save_to_db(posts)
    save_to_csv(posts)


if __name__ == "__main__":
    asyncio.run(main())
