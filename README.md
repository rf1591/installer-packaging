# installer-packaging

This repository will collect the various parts (code, tools, other content) 
that are necessary to build and package Seattle installers for the main 
operating systems and platforms we support.

Tools will include
* A new packaging script that generates Seattle installers for different platforms 
using the new build harness, and
* A new tool to sign and push software updates.

For this, we will refactor a few tools and code out of SeattleTestbed/dist, 
and make it compatible with SeattleTestbed/buildscripts.

Architectural discussion will follow below.

------
Overview of installer-package:

First of all, running initialize.py to download all files which we need to
DEPENDIENCES folder.

Secondly, running build.py to move all the platform-specific stuff and the
seattleinstaller into RUNNABLE folder. Since there is a new function( add
subdirectory) in new build scripts, we can move general files
to RUNNABLE/seattle_repy, and move specified files to RUNNABLE/seattle_mac,
RUNNABLE/seattle_linux... We need set config_build.txt based on the requirement
of each platforms,creating different subdirectories for different
platforms.

Finally, moving platform-specific stuff and the seattleinstaller under
RUNNABLE into base installer directory, then merging them together and create the
actual zip/gz/tar.gz files.
