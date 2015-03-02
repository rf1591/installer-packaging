# This will update the base installers used by seattelgeni from what
# is currently checked out as trunk. See constants below.
#
# You will need sudo privileges to use this. Don't run this as sudo, it will
# invoke sudo when it needs it.
#
# Usage: python ./rebuild_base_installers_for_seattlegeni.py VERSION_STRING
import sys
import string
import os
import shutil
import subprocess
import pwd
import grp
import glob

VERSION = sys.argv[1]

SOFTWARE_UPDATE_URL= 'http://blackbox.poly.edu/updatesite/'
PUBLIC_KEY_FILE= '/path/to/softwareupdater.publickey'
PRIVATE_KEY_FILE= '/path/to/softwareupdater.privatekey'

publickeyfile = open(PUBLIC_KEY_FILE, 'r')
content = publickeyfile.readline()
content.partition(" ")
e = content.partition(" ")[0]
n = content.partition(" ")[2]

SOFTWARE_UPDATE_KEY="{'e':" + e + ", 'n':" + n + "}"

REPO_PARENT_DIR='/home/cib/custominstallerbuilder/DEPENDENCIES'

BASE_INSTALLER_DIRECTORY='/home/cib/baseinstaller'

BASE_INSTALLER_ARCHIVE_DIR='/home/cib/baseinstaller/old_base_installers'

USER='cib'

# Check variables first
if VERSION == "":
    print "You must supply a version string."
    print "usage: " + sys.argv[0] + " version"
    sys.exit(1)

if SOFTWARE_UPDATE_URL == "":
    print "SOFTWARE_UPDATE_URL isn't set."
    sys.exit(1)

if not os.path.exists(BASE_INSTALLER_DIRECTORY):
    print "BASE_INSTALLER_DIRECTORY doesn't exist."
    sys.exit(1)

if not os.path.exists(BASE_INSTALLER_ARCHIVE_DIR):
    print "BASE_INSTALLER_ARCHIVE_DIR doesn't exist."
    sys.exit(1)

if not os.path.exists(REPO_PARENT_DIR):
    print "REPO_PARENT_DIR doesn't exist."
    sys.exit(1)

found = False
for line in open(REPO_PARENT_DIR + "/nodemanager/nmmain.py"):
    if VERSION in line:
        found = True
if found == False:
    print "You need to set the version string in " + REPO_PARENT_DIR + "/nodemanager/nmmain.py"
    sys.exit(1)

found = False
for line in open(REPO_PARENT_DIR + "/softwareupdater/softwareupdater.py"):
    if SOFTWARE_UPDATE_KEY in line:
        found = True
if found == False:
    print "Did not find the correct update key in " + REPO_PARENT_DIR + "/softwareupdater/softwareupdater.py"
    sys.exit(1)

found = False
for line in open(REPO_PARENT_DIR + "/softwareupdater/softwareupdater.py"):
    if "softwareurl = \"" + SOFTWARE_UPDATE_URL + "\"" in line:
        found = True
if found == False:
    print "Did not find the correct update url in " + REPO_PARENT_DIR + "/softwareupdater/softwareupdater.py"
    sys.exit(1)

try:
   pwd.getpwnam(USER)
except KeyError:
   print "User account " + USER + " does not exist."
   sys.exit(1)

# Now let's start building!
print "Archiving old base installers to " + BASE_INSTALLER_ARCHIVE_DIR
print "Warning: failure after this point may leave seattlegeni with no base installers!"

for files in glob.glob(BASE_INSTALLER_DIRECTORY + '/seattle_*' ):
    shutil.move(files, BASE_INSTALLER_ARCHIVE_DIR)

print "Building new base installers at " + BASE_INSTALLER_DIRECTORY

try:
    subprocess.call([sys.executable, REPO_PARENT_DIR + '/dist/make_base_installers.py', 'a', REPO_PARENT_DIR, PUBLIC_KEY_FILE, PRIVATE_KEY_FILE, BASE_INSTALLER_DIRECTORY, VERSION])
except:
    print "Building base installers failed."
    sys.exit(1)

print "Changing base installer symlinks used by seattlegeni."

os.chdir(BASE_INSTALLER_DIRECTORY)

if not os.path.exists("seattle_"+ VERSION +"_android.zip") or not os.path.exists("seattle_"+ VERSION +"_linux.tgz") or not os.path.exists("seattle_"+ VERSION +"_mac.tgz") or not os.path.exists("seattle_"+ VERSION +"_win.zip"):
    print "The base installers don't appear to have been created."
    sys.exit(1)

uid = pwd.getpwnam(USER).pw_uid
gid = grp.getgrnam(USER).gr_gid
for files in glob.glob('./seattle_*'):
    os.chown(files, uid, gid)

os.symlink("seattle_" + VERSION + "_android.zip", 'seattle_android.zip')
os.symlink("seattle_" + VERSION + "_linux.tgz", 'seattle_linux.tgz')
os.symlink("seattle_" + VERSION + "_mac.tgz", 'seattle_mac.tgz')
os.symlink("seattle_" + VERSION + "_win.zip", 'seattle_win.zip')

print 'New base installers created and installed for seattlegeni.'
