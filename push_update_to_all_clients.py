# Running this script will cause the updatesite directory checked by clients
# to be updated with the current files in the trunk directory. It will not
# automatically update trunk, so if you have a specfic revision checked out,
# that's what will be used. See constants below.
#
# You will need sudo privileges to use this. Don't run this as sudo, it will
# invoke sudo when it needs it.
#
# Usage: python ./push_update_to_all_clients.py
import sys
import string
import os
import time
import subprocess
import datetime
import calendar

TRUNK_DIR = '/home/cib/custominstallerbuilder/DEPENDENCIES'
PUBLIC_KEY_FILE = '/path/to/softwareupdater.publickey'
PRIVATE_KEY_FILE = '/path/to/softwareupdater.privatekey'

UPDATE_URL = 'http://blackbox.poly.edu/updatesite/'

UPDATESITE_DIR = '/var/www/updatesite'
DEBUG_UPDATESITE_DIR = UPDATESITE_DIR+ '-test'

# Sanity check to make sure the key embedded in softwareupdater.py is the same
# key we're signing with. The only time this would not be the case is if the
# update key is being changed.
publickeyfile = open(PUBLIC_KEY_FILE, 'r')
content = publickeyfile.readline()
e = content.partition(" ")[0]
n = content.partition(" ")[2]

UPDATE_PUBKEY_STRING = "{'e':" + e + ", 'n':" + n + "}"

found = False
for line in open(TRUNK_DIR + "/softwareupdater/softwareupdater.py"):
    if UPDATE_PUBKEY_STRING in line:
        found = True
if found == False:
    print "Did not find the correct update key in " + TRUNK_DIR + "/softwareupdater/softwareupdater.py"
    sys.exit(1)

found = False
for line in open(TRUNK_DIR + "/softwareupdater/softwareupdater.py"):
    if "softwareurl = \"" + UPDATE_URL + "\"" in line:
        found = True
if found == False:
    print "Did not find the correct update url in " + TRUNK_DIR + "/softwareupdater/softwareupdater.py"
    sys.exit(1)

if len(sys.argv) > 1:
    # Note that the -d option in update_software.py isn't a really convincing idea if you can
    # just pass a different directory.
    UPDATESITE_DIR = DEBUG_UPDATESITE_DIR
    print "An argument was provided. Using debug mode (so, putting files in " + UPDATESITE_DIR + ")."

# The update_software.py script does weird things if the directory doesn't already exist,
# such as creating a file with the name of the directory.
if not os.path.exists(UPDATESITE_DIR):
    try:
        os.mkdir(UPDATESITE_DIR)
    except:
        print "Failed to create missing directory " + UPDATESITE_DIR + "."
        sys.exit(1)

UPDATESITE_BACKUP_DIR = UPDATESITE_DIR + ".backups"

# Make sure there's a directory to backup the update directory to.
if not os.path.exists(UPDATESITE_BACKUP_DIR):
    os.mkdir(UPDATESITE_BACKUP_DIR)

# Backup the current updatesite.
DATE= calendar.timegm(time.strptime(time.strftime('%a %b %d %H:%M:%S %Y', time.localtime())))
print "Backing up " + UPDATESITE_DIR + " to " + UPDATESITE_BACKUP_DIR + os.path.sep + str(DATE)


subprocess.call([sys.executable, TRUNK_DIR + "/dist/update_software.py", TRUNK_DIR, PUBLIC_KEY_FILE, PRIVATE_KEY_FILE, UPDATESITE_DIR])

print "Done."
