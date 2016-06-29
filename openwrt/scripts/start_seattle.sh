#!/bin/sh

# Change to the seattle directory (this "cd" command allows the user to call the
#   script from any directory.
cd "`echo $0 | sed 's/start_seattle.sh//'`"

if grep "'seattle_installed': True" nodeman.cfg > /dev/null
then
    python nmmain.py &
    python softwareupdater.py &
else
    echo "seattle must first be installed before the start_seattle.sh script" \
	"can be run.  To install, run the install.sh script."
fi

# Wait a little so that it's unlikely that the processes launched in the
# background won't show up in the process list.
sleep 1

# Check to confirm that nmmain.py and softwareupdater.py are running, and echo
#   the status to the user.

if ps | grep nmmain.py | grep -v grep > /dev/null
then
if ps | grep softwareupdater.py | grep -v grep > /dev/null
    then
	echo "seattle has been started: $(date)"
    fi
else
    echo "seattle was not properly started."
    echo "If you continue to see this error for unknown reasons, please" \
	"contact the seattle development team."
fi
