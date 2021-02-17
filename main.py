import argparse
import datetime
import logging
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--folder", help="Log folder path")
parser.add_argument("--debug", help="Enable debug logging", action="store_true")
parser.add_argument("--days", help="Delete logs older than x days")
args, _ = parser.parse_known_args()

FOLDER = args.folder
DAYS = int(args.days) or 30
MB = 1024 * 1024

logging.basicConfig(
    handlers=[logging.StreamHandler(sys.stdout),],
    level=logging.DEBUG if args.debug else logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S%p %Z",
)

log_files = sorted(os.listdir(FOLDER))

removal_date = datetime.date.today() - datetime.timedelta(days=DAYS)
deleted_logs = 0
disk_space = 0
for log in log_files:
    log_date, _ = log.split("_")
    log_date = datetime.datetime.strptime(log_date, "%Y%m%d").date()
    if log_date < removal_date:
        file = os.path.join(FOLDER, log)
        filesize = os.stat(file).st_size
        os.remove(file)
        logging.debug(f"Removed {log}")
        deleted_logs += 1
        disk_space += filesize

disk_space = round(disk_space / MB, 3)
logging.info(
    f"Removed {deleted_logs} log files older then {removal_date} which used {disk_space} MB"
)

