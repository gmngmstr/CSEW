# CSEW
## Cyberpatriot Scoring Engine: Windows

CSEW is a scoring engine written in bash for scoring Windows CyberPatriot images. It is configured by adding scoring options into the `save_data.db` and moving everything to where it needs to be and setting up the scoring engine for auto running. It now includes a web page Score Report. It works (to varying degrees) with Windows 7, 8.1, 10.

## Features
CSEW is still a baby and it's rough around the edges, but so far it can score the following events:
- Disabling the Guest account
- Disabling the Administrator account
- Creating new users
- Deleting "bad" users
- Changing passwords on accounts
- Adding users to the administrator group
- Removing users from the administrator group
- Adding users to groups
- Removing users from groups
- Disabling do not require CTRL_ALT_DEL
- Enabling don't display last user
- Turning on the firewall for each profile
- Setting the minimum password age
- Setting the maximum password age
- Setting the maximum number of login tries
- Setting the lockout length
- Setting the lockout reset timer
- Setting the minimum password length
- Setting the maximum number of passwords to remember
- Enabling password complexity
- Disabling reversible password encryption
- Installing "good" programs
- Uninstalling "bad" programs
- Updating programs (WIP)
- Deleting prohibited files
- Removing backdoors (malicious services)
- Configuring the hosts files (WIP)
- Removing entries from taskschedualer (WIP)
- Installing an anti-virus other than Windows Defender
- Removing things from startup (WIP)
- Answering the forensics question correctly
- Changing update options (WIP)
- Adding or removing text from a file
- Removing programs and scripts from startup (WIP)

CSEW can also take away points for:
- Removing critical users
- Removing or stopping critical services
- Removing critical programs

CSEW can be run with "silent misses" which simulates a CyberPatriot round where you have no idea where the points are until you earn them. It can also be run with the silent misses turned off which is helpful when you are debugging or when you have very inexperienced students who might benefit from the help. This mode gives you a general idea where the points are missing. CSEW can also create a scoreboard report that can be sent to an FTP server and manipulated however you please.

## How to install
1. Go to [bitbucket](https://bitbucket.org/coastlinecollege/csew/src/master/configurator.exe) and download this file. The executable contains everything you need to setup a local scoring engine.
2. Run `configurator.exe` as an administrator.
3. Make your adjustments in `configurator.exe` that you want scored.
3. Once finished click `Write to Config` at the top left.
4. After you are satisfied that it is working how you want, you can delete the CSEW directory.

Notes:
The settings are saved in the `save_data.db` file as long as you have this file you can load the configuration at any time into the configurator and make changes

**Important Note**: Your students _will_ be able to see the vulnerabilities if you leave the CSEW folder behind or if they view the `save_data.db` file that is created in `C:/CyberPatriot/`. I tell my students where the file is and that they should stay away from it. It is practice, after all.

## Known issues and planned updates
- Write a sample explanation for a FTP server
- Make Readme generator and setting setter (Maybe)

## Source Code [Here](https://bitbucket.org/coastlinecollege/csew/src/master/)