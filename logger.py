import datetime
from datetime import datetime
from os import path

file_name_restrictions = r'\/:*?"<>|'


def start_log() -> str:
    today = datetime.today()
    log_path = f"logs//log ({today.year}-{today.month}-{today.day}).txt"
    log_num = 0
    while path.isfile(log_path):
        log_num += 1
        log_path = f"logs//log ({today.year}-{today.month}-{today.day}) - {log_num}.txt"
    with open(log_path, "w+") as file:
        file.write(f"MusicStreamAid Log, Date = ({today.year}-{today.month}-{today.day})\n")
    return log_path


def log_print(message: str) -> None:
    time_now = datetime.now()
    print(f"[{time_now.hour}:{time_now.minute}:{time_now.second}]: {message}")
