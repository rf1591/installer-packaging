# Ths will update the base installers used by seattelgeni from what
# is currently checked out as trunk. See constants below.
#
# You will need sudo privileges to use this. Don't run this as sudo, it will
# invoke sudo when it needs it.
#
# Usage: python ./rebuild_base_installers_for_seattlegeni.py version_STRING
import sys
import string
import os
import shutil
import subprocess
import pwd
import grp
import glob

version = sys.argv[1]

software_update_url= 'http://blackbox.poly.edu/updatesite/'
public_key_file= '/path/to/softwareupdater.publickey'
private_key_file= '/path/to/softwareupdater.privatekey'

publickeyfile = open(public_key_file, 'r')
content = publickeyfile.readline()
content.partition(" ")
e = content.partition(" ")[0]
n = content.partition(" ")[2]

software_update_key="{'e':" + e + ", 'n':" + n + "}"

repo_parent_dir='/home/cib/custominstallerbuilder/DEPENDENCIES'

base_installer_directory='/home/cib/baseinstaller'

base_installer_archive_dir='/home/cib/baseinstaller/old_base_installers'

user='cib'

# Check variables first
if version == "":
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

found = False
for line in open(repo_parent_dir + "/nodemanager/nmmain.py"):
    if version in line:
        found = True
if found == False:
    print "You need to set the version string in " + repo_parent_dir + "/nodemanager/nmmain.py"
    sys.exit(1)

found = False
for line in open(repo_parent_dir + "/softwareupdater/softwareupdater.py"):
    if software_update_key in line:
        found = True
if found == False:
    print "Did not find the correct update key in " + repo_parent_dir + "/softwareupdater/softwareupdater.py"
    sys.exit(1)

found = False
for line in open(repo_parent_dir + "/softwareupdater/softwareupdater.py"):
    if "softwareurl = \"" + software_update_url + "\"" in line:
        found = True
if found == False:
    print "Did not find the correct update url in " + repo_parent_dir + "/softwareupdater/softwareupdater.py"
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
    subprocess.call([sys.executable, repo_parent_dir + '/dist/make_base_installers.py', 'a', repo_parent_dir, public_key_file, private_key_file, base_installer_directory, version])
except:
    print "Building base installers failed."
    sys.exit(1)

print "Changing base installer symlinks used by seattlegeni."

os.chdir(base_installer_directory)

if not os.path.exists("seattle_"+ version +"_android.zip") or not os.path.exists("seattle_"+ version +"_linux.tgz") or not os.path.exists("seattle_"+ version +"_mac.tgz") or not os.path.exists("seattle_"+ version +"_win.zip"):
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

print 'New base installers created and installed for seattlegeni.'
