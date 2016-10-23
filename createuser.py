import argparse
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("user")

args = parser.parse_args()
logger = os.path.abspath(os.path.join(os.path.dirname(__file__), "logger.py"))

addcmd = "useradd -M -N -g honeypot -s {} {}".format(logger, args.user)
subprocess.call(addcmd, shell=True)
subprocess.call("passwd {}".format(args.user), shell=True)
#print addcmd
