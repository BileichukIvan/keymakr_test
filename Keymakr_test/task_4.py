import argparse
import logging
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


logging.basicConfig(
    filename="task_manager.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(String, nullable=False)
    status = Column(String, nullable=False)

    def __repr__(self):
        return (
            f"<Task(id={self.id}, title='{self.title}', description='{self.description}', "
            f"due_date='{self.due_date}', status='{self.status}')>"
        )


class TaskManager:
    def __init__(self, db_url="sqlite:///task.sqlite3"):
        self.engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_task(
        self, title: str, description: str, due_date: str, status: str
    ) -> None:
        """Adds a new task to the database."""

        session = self.Session()
        try:
            new_task = Task(
                title=title, description=description, due_date=due_date, status=status
            )
            session.add(new_task)
            session.commit()
            logging.info(f"Task '{title}' added to DB")
        except IntegrityError as exc:
            session.rollback()
            logging.error(f"Integrity violation error while adding task: {exc}")
            print(
                f"Error: Failed to add task due to integrity violation. Details: {exc}"
            )
        except SQLAlchemyError as exc:
            session.rollback()
            logging.error(f"Database error while adding task: {exc}")
            print(f"Error: Something went wrong while adding the task. Details: {exc}")
        finally:
            session.close()

    def update_task(self, task_id: int, status: str) -> None:
        """Updates the status of a task in the database."""

        session = self.Session()
        try:
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                task.status = status
                session.commit()
                logging.info(f"Task {task_id} status updated to {status}")
            else:
                logging.warning(f"Task with ID {task_id} not found")
        except SQLAlchemyError as exc:
            session.rollback()
            logging.error(f"Database error while updating task {task_id}: {exc}")
            print(
                f"Error: Something went wrong while updating the task. Details: {exc}"
            )
        finally:
            session.close()

    def delete_task(self, task_id: int) -> None:
        """Deletes a task from the database."""

        session = self.Session()
        try:
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                session.delete(task)
                session.commit()
                logging.info(f"Task {task_id} deleted successfully.")
            else:
                logging.warning(f"Task with ID {task_id} not found")
                print(f"Error: Task with ID {task_id} not found.")
        except SQLAlchemyError as exc:
            session.rollback()
            logging.error(f"Database error while deleting task {task_id}: {exc}")
            print(
                f"Error: Something went wrong while deleting the task. Details: {exc}"
            )
        finally:
            session.close()

    def list_tasks(self) -> None:
        """Lists all tasks in the database."""

        session = self.Session()
        try:
            tasks = session.query(Task).order_by(Task.due_date).all()
            if tasks:
                for task in tasks:
                    print(
                        f"ID: {task.id}, Title: {task.title}, Description: {task.description}, "
                        f"Due Date: {task.due_date}, Status: {task.status}"
                    )
                logging.info("Listed all tasks successfully")
            else:
                logging.warning("No tasks available in the database.")
                print("No tasks available.")
        except SQLAlchemyError as exc:
            logging.error(f"Database error while listing tasks: {exc}")
            print(f"Error: Something went wrong while listing tasks. Details: {exc}")
        finally:
            session.close()


def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments."""

    parser = argparse.ArgumentParser(description="Task Manager CLI")
    parser.add_argument("--add", action="store_true", help="Add new task")
    parser.add_argument("--update", type=int, help="Update task status by ID")
    parser.add_argument("--delete", type=int, help="Delete task by ID")
    parser.add_argument("--list", action="store_true", help="List all tasks")
    parser.add_argument("--title", type=str, help="Task title")
    parser.add_argument("--description", type=str, help="Task description")
    parser.add_argument("--due_date", type=str, help="Task due date")
    parser.add_argument(
        "--status",
        choices=["pending", "in_progress", "completed"],
        type=str,
        help="Task status",
    )

    return parser.parse_args()


def main():
    """Main function to run the program."""

    args = parse_arguments()
    task_manager = TaskManager()

    if args.add:
        if args.title and args.due_date:
            task_manager.add_task(
                args.title,
                args.description or "",
                args.due_date,
                args.status or "pending",
            )
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
