import re
import sys
import logging
from collections import Counter


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def parse_log_line(line: str) -> dict[str, str] | None:
    """Split log line into groups and return a dictionary with the groups."""
    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[.*\] "\w+ (?P<url>\S+) .*" (?P<status>\d{3}) (?P<size>\d+)'
    )
    match = log_pattern.match(line)
    return match.groupdict() if match else None


def analyze_log(file_path: str) -> None:
    """Analyst log file"""
    ip_counter = Counter()
    client_error_counter = Counter()
    server_error_counter = Counter()
    total_size = 0
    count = 0

    try:
        logging.info(f"Opening log file: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                data = parse_log_line(line)
                if data:
                    ip_counter[data["ip"]] += 1
                    status_code = int(data["status"])

                    if data["size"] != "-" and data["size"].isdigit():
                        total_size += int(data["size"])
                        count += 1
                    else:
                        logging.warning(f"Invalid size value: {data['size']}")

                    if 400 <= status_code < 500:
                        client_error_counter[status_code] += 1
                    elif 500 <= status_code < 600:
                        server_error_counter[status_code] += 1

        logging.info("Successfully processed the log file.")
    except OSError as e:
        logging.error(f"Error opening the log file '{file_path}': {e}")
        return None

    logging.info("Calculating top 5 IP addresses with the most requests.")
    for ip, freq in ip_counter.most_common(5):
        print(f"{ip}: {freq} requests\n")
        logging.debug(f"IP: {ip}, Requests: {freq}")

    logging.info("Calculating most frequent client error codes (4xx).")
    for status, freq in client_error_counter.most_common(5):
        print(f"{status}: {freq} times\n")
        logging.debug(f"Client Error Code: {status}, Frequency: {freq}")

    logging.info("Calculating most frequent server error codes (5xx).")
    for status, freq in server_error_counter.most_common(5):
        print(f"{status}: {freq} times\n")
        logging.debug(f"Server Error Code: {status}, Frequency: {freq}")

    avg_size = total_size / count if count > 0 else 0
    logging.info(f"Average size of responses calculated: {avg_size:.2f} bytes")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python task_3.py access.log")
        sys.exit(1)
    analyze_log(sys.argv[1])
