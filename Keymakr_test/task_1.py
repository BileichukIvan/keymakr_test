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
    """Async function to fetch a single post from API"""
    try:
        async with session.get(f"{API_URL}/{post_id}") as response:
            if response.status == 200:
                return await response.json()
            else:
                logging.warning(f"Error fetching post {post_id}: {response.status}")
                return None
    except asyncio.TimeoutError:
        logging.error(f"Timeout fetching post {post_id}")
    except aiohttp.ClientError:
        logging.error(f"Error fetching post {post_id}")
    return None


async def fetch_all_posts() -> list[dict | None]:
    """Async function to fetch all posts from API"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_posts(session, post_id) for post_id in range(1, 101)]
        all_posts = await asyncio.gather(*tasks)
        valid_posts = [post for post in all_posts if post]
        return valid_posts


def save_to_db(posts: list[dict | None]) -> None:
    """Saves posts in sqlite3 database"""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    title TEXT,
                    body TEXT
                )
            """
        )

        cursor.executemany(
            """
                INSERT OR REPLACE INTO posts (id, user_id, title, body)
                VALUES (:id, :userId, :title, :body)
            """,
            posts,
        )

        conn.commit()
        logging.info("Posts successfully saved to database")
    except sqlite3.Error as e:
        logging.error(f"An error occurred while working with the database: {e}")
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed")


def save_to_csv(posts: list[dict | None]) -> None:
    """Saves data in CSV format"""
    try:
        with open(CSV_NAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "userId", "title", "body"])
            writer.writeheader()
            writer.writerows(posts)
        logging.info("Posts successfully saved to CSV")
    except OSError as e:
        logging.error(f"An error occurred while writing to the CSV file: {e}")


async def main() -> None:
    """Main function to run the program"""
    logging.info("Starting fetching process")
    posts = await fetch_all_posts()
    save_to_db(posts)
    save_to_csv(posts)


if __name__ == "__main__":
    asyncio.run(main())
