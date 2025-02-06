import re
import sys
from collections import Counter


def parse_log_line(line: str) -> dict[str, str] | None:
    """Розбирає рядок з логами на його складові"""
    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[.*\] "\w+ (?P<url>\S+) .*" (?P<status>\d{3}) (?P<size>\d+)'
    )
    match = log_pattern.match(line)
    return match.groupdict() if match else None


def analyze_log(file_path: str) -> None:
    """"Аналізує лог файл"""
    ip_counter = Counter()
    error_counter = Counter()
    total_size = 0
    count = 0

    with open(file_path, "r") as file:
        for line in file:
            data = parse_log_line(line)
            if data:
                ip_counter[data["ip"]] += 1
                status_code = int(data["status"])
                if 400 <= status_code < 500:
                    error_counter[status_code] += 1
                    total_size += int(data["size"])
                    count += 1

    print("Top 5 IP addresses with most requests:\n")
    for ip, freq in ip_counter.most_common(5):
        print(f"{ip}: {freq} requests\n")

    print(f"Most frequent error codes:\n")
    for status, freq in error_counter.most_common(5):
        print(f"{status}: {freq} times\n")

    avg_size = total_size / count if count > 0 else 0
    print(f"Average size of responses is: {avg_size:.2f} bytes")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python task_3.py access.log")
        sys.exit(1)
    analyze_log(sys.argv[1])
