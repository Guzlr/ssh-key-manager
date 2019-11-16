#!/usr/bin/python

import sys
import subprocess
import getpass
from pprint import pprint

import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

username = getpass.getuser()
hosts = [x.strip() for x in open('push_hostlist.txt') if x.strip()]

for host in hosts:
   # Check if a host in the list is 'commented out'
   if host[0] == "#":
      pass
      #print ('Ignoring host: {}'.format(host[1:]))
   else:
      print ('Processing host: {}'.format(host))

      # Check the host responds to ping - avoiding scp timout errors/lockups
      cmd = ["ping", "-c 1", "-W 1", host]

      try:
         subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
      except subprocess.CalledProcessError:
         print ("   Host offline: {}".format(host))
         continue

      # Copy the authorized_keys file from the host
      cmd = ["scp", "{}:~/.ssh/authorized_keys".format(host), "./authorized_keys.in"]

      try:
         subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
      except subprocess.CalledProcessError:
         print ("   scp inbound failed: {}".format(host))
         continue

      # Read in the copied authorized_keys file and the user-specific update list
      target = [x.strip() for x in open('authorized_keys.in')]
      updates = [x.strip() for x in open('{}_public_keys.txt'.format(username))]

      # Selectively update the list of keys - add each update if it doesn't already exist
      for update in updates:
         if len(update):
            if update[0] == "#":
               comment = update
            else:
               key = update
               if key in target:
                  pass
                  #print ("Skipping key {}".format(comment))
               else:
                  print ("  - Adding new Key for {}".format(comment))
                  target.append("")
                  target.append(comment)
                  target.append(key)

      # Write the updated list of keys out to a file
      with open('authorized_keys.out', 'w') as f:
         for rec in target:
            f.write("{}\n".format(rec))

      # Copy the updated authorized_keys file back to the host
      cmd = ["scp", "./authorized_keys.out", "{}:~/.ssh/authorized_keys".format(host)]

      try:
         subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
      except subprocess.CalledProcessError:
         print ("   scp outbound failed: {}".format(host))
         continue
      
      # Delete the temporary files
      cmd = ["rm", "./authorized_keys.in", "./authorized_keys.out"]

      try:
         subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
      except subprocess.CalledProcessError:
         print ("Error deleting temporary files.")

