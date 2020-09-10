# CSEW (WIP)
## Cyberpatriot Scoring Engine: Windows

CSEW is a scoring engine written in bash for scoring Windows CyberPatriot images. It is configured by adding scoring options into the `save_data.json` and moving everything to where it needs to be and setting up the scoring engine for auto running. It now includes a web page Score Report. It works (to varying degrees) with Windows 7, 8.1, 10.

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
- Deleting prohibited files
- Removing backdoors (malicious services)
- Configuring the hosts files (WIP)
- Removing entries from taskschedualer (WIP)
- Installing an anti-virus other than Windows Defender
- Removing things from startup (WIP)
- Answering the forensics question correctly
- Changing update options (WIP)
- Adding or removing text from a file

CSEW can also take away points for:
- Deleting "good" users

CSEW can be run with "silent misses" which simulates a CyberPatriot round where you have no idea where the points are until you earn them. It can also be run with the silent misses turned off which is helpful when you are debugging or when you have very inexperienced students who might benefit from the help. This mode gives you a general idea where the points are missing. CSEW can also create a scoreboard report that can be sent to an FTP server and manaipulated however you please.

## How to install using git
1. Set up your image and put your vulnerabilities in place.
2. Clone into CSEW by typing: `git clone https://github.com/gmngmstr/CSEWv2.git`
3. Run `CSEW\Run Files\configurator.exe` as administrator to set up the config file. 
4. Once finished click `Write to Config` at the bottom of the page
5. After you are satisfied that it is working how you want, you can delete the CSEW directory.

## How to install without git
1. To install the scoring engine extract the folder to the desktop of the windows image
2. Run `CSEW\Run Files\configurator.exe` as administrator to set up the config file. 
3. To edit the configuration of the scoring engine type `sudo python configurator.py` in the terminal
	This will launch the GUI for configuring the scoring settings
4. Once finished click `Write to Config` at the bottom of the page
5. After you are satisfied that it is working how you want, you can delete the CSEW directory.

Notes:
The settings are saved in the `save_data.json` file as long as you have this file you can load the configuration at any time into the configurator and make changes

**Important Note**: Your students _will_ be able to see the vulnerabilities if you leave the CSEW folder behind or if they view the `save_data.json` file that is created in `C:/CyberPatriot/`. I tell my students where the file is and that they should stay away from it. It is practice, after all.

## Known issues and planned updates
- Write a sample explanation for a FTP server
- Update all of the explanations
- Make Readme generator and setting setter (Maybe)