__author__ = 'pandazxx'


from u115 import API
import logging
import os
import time
import sys

logger = logging.getLogger(__name__)


logging.basicConfig(level=logging.DEBUG)

print "Please input username:"
username = sys.stdin.readline().rstrip("\n")
password = sys.stdin.readline().rstrip("\n")

remote_path = "tobe_downloaded"
remote_backup_path = "bak"

local_path = "~/Downloads/u115"

interval = 60

local_path = os.path.expanduser(local_path)

logger.debug("USERNAME: %s", username)
logger.debug("REMOTE_DIR: %s", remote_path)
logger.debug(("LOCALDIR: %s", local_path))


class MachineError(Exception):
    pass


if not os.path.exists(local_path):
    os.makedirs(local_path)

if not os.path.isdir(local_path):
    raise MachineError("Destination dir %s is exists and not a directory" % local_path)

api = API()

if not api.login(username, password):
    raise MachineError("Login failed")

remote_dir = api.find_directory(remote_path)

backup_dir = api.find_directory(remote_backup_path)

if not remote_dir:
    raise MachineError("Cannot find remote dir %s" % remote_path)

if not backup_dir:
    raise MachineError("Cannot find remote backup dir %s" % remote_backup_path)

while True:
    try:
        logger.info("Checking remote dir %s for download files", remote_path)
        remote_dir.reload()
        sub_files = remote_dir.list(count=remote_dir.count)
        if logger.level >= logging.DEBUG:
            for f in sub_files:
                logger.debug("Found file %s", f.name)
        for f in sub_files:
            logger.info("Downloading %s", f.name)
            f.download(path=local_path)
            f.move_to(backup_dir)
        else:
            logger.info("All files from %s are downloaded", remote_path)
        logger.info("Sleep %d seconds", interval)
    except:
        api.login(username, password)
    time.sleep(interval)



