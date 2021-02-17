import argparse
import datetime
import glob
import logging
import os
import sys


parser = argparse.ArgumentParser()
parser.add_argument("--folder", help="Log folder path")
parser.add_argument("--debug", help="Enable debug logging", action="store_true")
parser.add_argument(
    "--days", type=int, default=30, help="Delete logs older than x days"
)
ARGS, _ = parser.parse_known_args()


logging.basicConfig(
    handlers=[logging.StreamHandler(sys.stdout),],
    level=logging.DEBUG if ARGS.debug else logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S%p %Z",
)


def file_datestamp(file):
    """Pull datestamp from filename or use modified date if not present"""
    try:
        name = os.path.basename(file)
        date_str, _ = name.split("_")
        log_date = datetime.datetime.strptime(date_str, "%Y%m%d").date()
    except ValueError:
        mtime = os.stat(file).st_mtime
        log_date = datetime.datetime.fromtimestamp(mtime).date()
    return log_date


def convert_size(size_bytes):
    """Convert filesize in bytes to human readable units"""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s}{size_name[i]}"


def rm_old_logs(logs):
    """Delete log files older than a specified date"""
    rm_date = datetime.date.today() - datetime.timedelta(days=ARGS.days)
    deleted = 0
    space = 0
    for log in logs:
        if file_datestamp(log) < rm_date:
            space += os.stat(log).st_size
            os.remove(log)
            deleted += 1
            logging.debug(f"Removed {log}")
    space = convert_size(space)
    logging.info(f"Removed {deleted} logs ({space}) older than {rm_date}")


if __name__ == "__main__":
    logs = glob.glob(f"{ARGS.folder}/*.log")
    rm_old_logs(logs)
