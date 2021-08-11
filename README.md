# palo-alto_remove-zone
Python script that iterates through the security post rules in a device-group and removes the user-specified zone from both source and destination fields. 

Necessary Libraries and Programs:
----------------------------------
* Python3.7+
* requests
* JSON
* urllib3


User-dependant settings
----------------------------------
* You will need to generate and reference your own API key (see my API key generation script to get one!)
* You will need to edit the correct path to your 'creds.json' file (line 17)
* You will need to edit the correct path for the text files used for pre- and post-rule validation (lines 30, 31), if you want to use them.
* You will need to specify the path for the edited rule name file. This file is used for auditing purposes if we need to
  re-edit the rules to add the zones back in. (line 32)


Instructions for use
----------------------------------
1. Open terminal or PowerShell window
2. Navigate to the locations the repo with this script resides
    2a. cd /path/to/repo
3. Run the script using "python script_name.py" (Windows) or "./script_name.py" (MacOS/Linux)
    3a. If using MacOS or Linux, ensure that you change the permissions for Python3 to run the script
        ("chmod a+x script_name.py")
4. Follow the on-screen prompts. You will be asked for typing out the name of the device-group you need to parse and
   the name of the zone you need to remove.
