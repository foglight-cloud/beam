#!/usr/bin/env python3

import argparse
import getopt
import json
import os
import re
import requests
import socket
import sys
import yaml

config = None

def update():
  # Fetch database if some cache condition is met
  r = requests.get('https://logs.foglight.cloud/api/snapshot')
  with open(os.path.join(os.path.expanduser('~'), '.fl/all.db'), 'w') as f:
    f.write(r.text)

def read_stdin():
  # Read database
  global config
  db = {}
  local = os.path.join(os.path.expanduser('~'), '.fl/all.db')
  if not os.access(local, os.R_OK):
    update()
  with open(local, 'r') as f:
    for line in f:
      flid,regex = line.split("|", 1)
      db[regex.strip()] = flid

  while 1:
    line = sys.stdin.readline().rstrip('\n')
    if not line: continue;

    # Check line matches database
    for key in db:
      # if so, send to beam server
      if re.match(key, line):
        headers = {'charset': 'utf-8'}
        url = config['beam_baseuri'] + '/api/message'
        data = {}
        data['message'] = line
        data['hostname'] = socket.gethostname()
        data['id'] = db.get(key)
        requests.post(url, json=data, headers=headers)

    print(line)

def check_config():
  global config
  cfg = os.path.join(os.path.expanduser('~'), '.fl/config.yml')
  if not os.access(cfg, os.R_OK):
    with open(cfg, 'w') as f:
      f.write("beam_baseuri: http://localhost:8080")
  else:
    with open(cfg, 'r') as f:
      config = yaml.load(f)

def main():
  try:
    # Create config directory
    os.makedirs(os.path.join(os.path.expanduser('~'), '.fl'), exist_ok=True)

    # Check command line options
    opts, args = getopt.getopt(sys.argv[1:], '', ['update'])
    for opt,val in opts:
      if opt == '--update':
        update()
    if not opts:
      check_config()
      read_stdin()
  except (KeyboardInterrupt, SystemExit):
    sys.exit(0)
  except getopt.error as msg:
    sys.stdout = sys.stderr
    print(msg)

if __name__ == '__main__':
  main()

