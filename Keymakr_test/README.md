# Keymakr Test task
This repository contains the implementation of four test tasks along with additional files for the completed tasks.

Tasks list:
- **Task 1:** Working with APIs and Multithreading
Write a script that fetches data from an API (e.g., JSONPlaceholder) in parallel and saves it to an SQLite database.
  - Fetched data are stored in posts.sqlite3 and posts.csv files


- **Task 2:** File Processing and XML/JSON Conversion
You have a directory with XML files containing product data. Write a script that parses XML files, converts them into JSON, and saves them in a new directory.
    - Input **.xml** files are store in xml_input folder
    - Output **.json** files are stored in json_output folder

  You can run script with this command ```python task_2.py --input-dir ./xml_input --output-dir ./json_output```


- **Task 3:** CLI Tool for Log Analysis
Create a Python script that analyzes web server logs in Nginx format.
    - Example logs for analysis stored in access.log file

  You can run script with this command ```python task_3.py access.log```


- **Task 4:** Task Manager with any lite db (sqlite/…)
Develop a simple task management system using Python and lite db. How to Use:
    - Add a task:```python task_4.py --add --title "Task Title" --due "2025-02-10" --description "Task Description"```
    - Update task status: ```python task_4.py --update 1 --status "completed"```
    - Delete a task: ```python task_4.py --delete 1```
    - List tasks: ```python task_4.py --list```

    All logs are stored in the **task_manager.log** file. Also, all data is stored inside **task.sqlite3** file
# Installation

- **Clone the repository**
```bash
git clone https://github.com/BileichukIvan/keymakr_test.git
cd keymakr_test
```
- **Set Up the Virtual Environment**\
Create and activate a Python virtual environment to isolate project dependencies:

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```
**On Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```
  
- **Install Dependencies**\
Once your virtual environment is active, install the required dependencies:
```bash
pip install -r requirements.txt
```

