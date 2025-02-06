import sqlite3
import logging
import argparse

logging.basicConfig(
    filename="task_manager.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


class TaskManager:
    def __init__(self, db_name="task.sqlite3") -> None:
        self.db_name = db_name
        self.create_table()


    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT NOT NULL,
            status TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()


    def add_task(
            self, title: str, description:str, due_date:str, status:str
    ) -> None:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (title, description, due_date, status)
            VALUES (?, ?, ?, ?)
        """, (title, description, due_date, status))
        conn.commit()
        conn.close()
        logging.info(f"Task '{title}' added to DB")


    def update_task(self, task_id: int, status:str) -> None:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tasks SET status = ? WHERE id = ?
        """, (status, task_id))
        conn.commit()
        conn.close()
        logging.info(f"Task {task_id} status updated to {status}")


    def delete_task(self, task_id: int) -> None:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM tasks WHERE id = ?
        """, (task_id,))
        conn.commit()
        conn.close()


    def list_tasks(self) -> None:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM tasks ORDER BY due_date
        """)
        tasks = cursor.fetchall()
        conn.close()

        for task in tasks:
            print(f"ID: {task[0]}, Title: {task[1]}, Description{task[2]}, Due Date: {task[3]}, Status: {task[4]}")
        logging.info("Listed all tasks")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    parser.add_argument("--add", action="store_true", help="Add new task")
    parser.add_argument("--update", type=int, help="Update task status by ID")
    parser.add_argument("--delete", type=int, help="Delete task by ID")
    parser.add_argument("--list", action="store_true", help="List all tasks")
    parser.add_argument("--title", type=str, help="Task title")
    parser.add_argument("--description", type=str, help="Task description")
    parser.add_argument("--due_date", type=str, help="Task due date")
    parser.add_argument(
        "--status", choices=["pending", "in_progress", "completed"], type=str, help="Task status"
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    task_manager = TaskManager()

    if args.add:
        if args.title and args.due_date:
            task_manager.add_task(args.title, args.description or "", args.due_date, args.status or "pending")
        else:
            print("Title and due date are required to add a task.")

    elif args.update:
        if args.status:
            task_manager.update_task(args.update, args.status)
        else:
            print("Please provide a status to update the task.")

    elif args.delete:
        task_manager.delete_task(args.delete)

    elif args.list:
        task_manager.list_tasks()


if __name__ == "__main__":
    main()