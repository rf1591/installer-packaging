#!/bin/sh

cd "`echo $0 | sed 's/stop_seattle.sh//'`"

python stop_all_seattle_processes.py


# Check to confirm that nmmain.py and softwareupdater.py have been killed and
#   echo the status to the user.

if ! ps | grep nmmain.py | grep -v grep > /dev/null
then
    if ! ps | grep softwareupdater.py | grep -v grep > /dev/null
    then
	echo "seattle has been stopped: $(date)"
    fi
else
    echo "seattle could not be stopped for an unknown reason."
    echo "If you continue to see this error, please contact the seattle" \
	"development team."
fi