'''
This will update the base installers used by seattelgeni from what
is currently checked out as trunk. See constants below.

You will need sudo privileges to use this. Don't run this as sudo, it will
invoke sudo when it needs it.

Usage: python ./rebuild_base_installers_for_seattlegeni.py version_STRING
'''
import sys
import string
import os
import shutil
import subprocess
import pwd
import grp
import glob

from softwareupdater import softwareupdatepublickey
from softwareupdater import softwareurl
from nmmain import version

import package_installers

software_update_url= 'http://blackbox.poly.edu/updatesite/'
public_key_file = '/path/to/publickey'
private_key_file = '/path/to/privatekey'

def rebuild_base_installers(newversion):
  publickeyfile = open(public_key_file, 'r')
  content = publickeyfile.readline()
  content.partition(" ")
  e = content.partition(" ")[0]
  n = content.partition(" ")[2]

  software_update_key = {}
  software_update_key['e'] = int(e)
  software_update_key['n'] = int(n)

  repo_parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../DEPENDENCIES")

  base_installer_directory ='/home/cib/baseinstaller'

  base_installer_archive_dir ='/home/cib/baseinstaller/old_base_installers'

  user='cib'

  # Check variables first
  if newversion == "":
    print "You must supply a version string."
    print "usage: " + sys.argv[0] + " version"
    sys.exit(1)

  if software_update_url == "":
    print "software_update_url isn't set."
    sys.exit(1)

  if not os.path.exists(base_installer_directory):
    print "base_installer_directory doesn't exist."
    sys.exit(1)

  if not os.path.exists(base_installer_archive_dir):
    print "base_installer_archive_dir doesn't exist."
    sys.exit(1)

  if not os.path.exists(repo_parent_dir):
    print "repo_parent_dir doesn't exist."
    sys.exit(1)

  if not version:
    print "You need to set the version string in nmmain.py"
    sys.exit(1)

  if not version == newversion:
    print "You need to set the version string which is same as the version string in nmmain.py"
    sys.exit(1)

  if not software_update_url == softwareurl:
    print "Did not find the correct update url in softwareupdater.py" 
    sys.exit(1)

  if not software_update_key == softwareupdatepublickey:
    print "Did not find the correct update key in softwareupdater.py"
    sys.exit(1)

  try:
    pwd.getpwnam(user)
  except KeyError:
   print "user account " + user + " does not exist."
   sys.exit(1)

  # Now let's start building!
  print "Archiving old base installers to " + base_installer_archive_dir
  print "Warning: failure after this point may leave seattlegeni with no base installers!"

  for files in glob.glob(base_installer_directory + '/seattle_*' ):
    shutil.move(files, base_installer_archive_dir)

  print "Building new base installers at " + base_installer_directory

  try:
    package_installers.package_installers(base_installer_directory, version, private_key_file, public_key_file)
  except:
    print "Building base installers failed."
    sys.exit(1)

  print "Changing base installer symlinks used by seattlegeni."

  os.chdir(base_installer_directory)

  if not os.path.exists("seattle_"+ version +"_android.zip") or not os.path.exists("seattle_"+ version +"_linux.tgz") or not os.path.exists("seattle_"+ version +"_mac.tgz") or not os.path.exists("seattle_"+ version +"_win.zip")or not os.path.exists("seattle_"+ version +"_win_mob.zip"):
    print "The base installers don't appear to have been created."
    sys.exit(1)

  uid = pwd.getpwnam(user).pw_uid
  gid = grp.getgrnam(user).gr_gid
  for files in glob.glob('./seattle_*'):
    os.chown(files, uid, gid)

  os.symlink("seattle_" + version + "_android.zip", 'seattle_android.zip')
  os.symlink("seattle_" + version + "_linux.tgz", 'seattle_linux.tgz')
  os.symlink("seattle_" + version + "_mac.tgz", 'seattle_mac.tgz')
  os.symlink("seattle_" + version + "_win.zip", 'seattle_win.zip')
  os.symlink("seattle_" + version + "_win_mob.zip", 'seattle_win_mob.zip')

  print 'New base installers created and installed for seattlegeni.'

def main():
  newversion = sys.argv[1]
  rebuild_base_installers(newversion)

if __name__ == '__main__':
  main()
