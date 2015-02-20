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

