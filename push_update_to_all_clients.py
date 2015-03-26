'''
Running this script will cause the updatesite directory checked by clients
to be updated with the current files in the trunk directory. It will not
automatically update trunk, so if you have a specfic revision checked out,
that's what will be used. See constants below.

You will need sudo privileges to use this. Don't run this as sudo, it will
invoke sudo when it needs it.

Usage: python ./push_update_to_all_clients.py
'''

import sys
import string
import os
import time
import subprocess
import datetime
import calendar
import shutil

from softwareupdater import softwareupdatepublickey
from softwareupdater import softwareurl

import package_installers

from repyportability import *
add_dy_support(locals())

dy_import_module_symbols("rsa.r2py")

dependencies_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../DEPENDENCIES")

public_key_file = ''

private_key_file = ''

update_url = 'http://blackbox.poly.edu/updatesite/'

updatesite_dir = '/var/www/updatesite'

# Sanity check to make sure the key embedded in softwareupdater.py is the same
# key we're signing with. The only time this would not be the case is if the
# update key is being changed.
def push_update():  
  update_pubkey_string = rsa_file_to_publickey(public_key_file)

  if not update_url == softwareurl:
    print "Did not find the correct update url in softwareupdater.py" 
    sys.exit(1)

  if not update_pubkey_string == softwareupdatepublickey:
    print "Did not find the correct update key in softwareupdater.py"
    sys.exit(1)

  # The update_software.py script does weird things if the directory doesn't already exist,
  # such as creating a file with the name of the directory.
  if not os.path.exists(updatesite_dir):
    try:
      os.mkdir(updatesite_dir)
    except:
      print "Failed to create missing directory " + updatesite_dir + "."
      sys.exit(1)

  updatesite_backup_dir = updatesite_dir + ".backups"

  # Make sure there's a directory to backup the update directory to.
  if not os.path.exists(updatesite_backup_dir):
    os.mkdir(updatesite_backup_dir)

  # Backup the current updatesite.
  date = calendar.timegm(time.strptime(time.strftime('%a %b %d %H:%M:%S %Y', time.localtime())))

  print "Backing up " + updatesite_dir + " to " + updatesite_backup_dir + os.path.sep + str(date)

  shutil.copytree(updatesite_dir,updatesite_backup_dir + os.path.sep + str(date))

  package_installers.prepare_gen_files(updatesite_dir,private_key_file,public_key_file)
  
  print "Done."

def main():
  if not public_key_file:
    print "public_key_file isn't set." 
    sys.exit(1)

  if not private_key_file:
    print "private_key_file isn't set." 
    sys.exit(1)

  push_update()

if __name__ == '__main__':
  main()
