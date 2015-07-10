# installer-packaging

This repository provides the various parts (code, tools, other content) 
that are necessary to build and package Seattle *base installers* for the main 
operating systems and platforms we support. In their current form, the tools 
are intended for use only in the 
[Custom Installer Builder](https://github.com/SeattleTestbed/custominstallerbuilder)
and/or CIB admins, not end users.

Each base installer contains the Seattle runtime, nodemanager, etc., and all 
of the platform abstractions required to install, run, and autostart Seattle, 
*but* lacks the user keys (in the form of the `vesselinfo` file) required to 
actually perform the installation and provide remote-accessible resources 
afterwards.
The CIB knows how to create this `vesselinfo` file and add it so that the resulting 
installer is complete.

Tools include
* A packaging script that generates Seattle installers for different platforms, and
* A script to sign and "push" (put in the appropriate web server dir) software updates.


------
# Using this repo

Clone this repo, then run the initialization script (which git-clones all 
of installer-packaging's dependencies) and build script (which prepares 
the Python source files and platform-specific installer stuff).

```bash
$ git clone https://github.com/SeattleTestbed/installer-packaging
$ cd installer-packaging/scripts
$ python initialize.py
$ python build.py
```

Several new directories are created thus:
* `../RUNNABLE` now contains the script to build new base installers,
* `../RUNNABLE/seattle_repy` holds the general Seattle runtime, nodemanager, 
etc.,
* and `../RUNNABLE/seattle_linux`, `../RUNNABLE/seattle_mac` and so on 
have the platform-specific files.

The `rebuild_base_installers` script then copies the generic and 
platform-specific stuff into base installer directories, and creates the
actual zip/gz/tar.gz files that the Custom Installer Builder expects.
