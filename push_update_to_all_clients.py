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

trunk_dir = '/home/cib/custominstallerbuilder/DEPENDENCIES'
public_key_file = '/path/to/softwareupdater.publickey'
private_key_file = '/path/to/softwareupdater.privatekey'

update_url = 'http://blackbox.poly.edu/updatesite/'

updatesite_dir = '/var/www/updatesite'
debug_updatesite_dir = updatesite_dir+ '-test'

# Sanity check to make sure the key embedded in softwareupdater.py is the same
# key we're signing with. The only time this would not be the case is if the
# update key is being changed.
publickeyfile = open(public_key_file, 'r')
content = publickeyfile.readline()
e = content.partition(" ")[0]
n = content.partition(" ")[2]

update_pubkey_string = "{'e':" + e + ", 'n':" + n + "}"

found = False
for line in open(trunk_dir + "/softwareupdater/softwareupdater.py"):
    if update_pubkey_string in line:
        found = True
if found == False:
    print "Did not find the correct update key in " + trunk_dir + "/softwareupdater/softwareupdater.py"
    sys.exit(1)

found = False
for line in open(trunk_dir + "/softwareupdater/softwareupdater.py"):
    if "softwareurl = \"" + update_url + "\"" in line:
        found = True
if found == False:
    print "Did not find the correct update url in " + trunk_dir + "/softwareupdater/softwareupdater.py"
    sys.exit(1)

if len(sys.argv) > 1:
    # Note that the -d option in update_software.py isn't a really convincing idea if you can
    # just pass a different directory.
    updatesite_dir = debug_updatesite_dir
    print "An argument was provided. Using debug mode (so, putting files in " + updatesite_dir + ")."

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


subprocess.call([sys.executable, trunk_dir + "/dist/update_software.py", trunk_dir, public_key_file, private_key_file, updatesite_dir])

print "Done."
