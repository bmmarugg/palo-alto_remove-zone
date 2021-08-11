#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
# v2.0 | See changelog.txt in this scripts repo for full details

# This script can be edited to target any device-group and any zone. It is 100% necessary to ensure correct spelling and
# syntax when defining these elements, so be very sure the device-group, rule name, and zone name are exactly as they
# appear in Panorama. Capitalization does not matter.

import json
from pprint import pprint
import requests
import urllib3

# Disables terminal/PowerShell SSL Cert validation warning messages - super annoying
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Imports credentials securely from your local creds file
with open("PATH/TO/creds.json") as credentials:
    creds = json.load(credentials)

api_key = creds['pan_api_key']
base_url = "https://YOUR-PANORAMA-URL-HERE/restapi/v9.1"

headers = {
    'X-PAN-KEY': f'{api_key}',
    'content-type': 'application/json'
}

# These can be used to print the values of the rules BEFORE the zone removal and AFTER the zone removal for
# side-by-side comparisons for validation
#pre_zone_remove_outfile = open("PATH/TO/pre_zone-remove_rules.json", "w")
#post_zone_remove_outfile = open("PATH/TO/post_zone-remove_rules.json", "w")
#old_rule_log = open("PATH/TO/zone-edited-rules.txt", "w+")

device_group_list = ["device-group-1", "device-group-1", "etc"]

for dg in device_group_list:
    pprint(dg.replace("'", ""))

user_dg = input('''
Type the name of the device-group you need to remove the zone from exactly as it appears above: 
''')

user_zone = input('''
Type the name of the zone you need to remove: 
''')

# The API request that fetches ALL of the rules in the specified device-group
get_rules = requests.get(f"{base_url}/policies/securitypostrules?location=device-group&device-group={user_dg}",
                         verify=False, headers=headers)

# Unpacks the JSON data of the response
vpn_rules = get_rules.json()

# This section parses through all of the rules and makes a list of only the rules that use the zone we want to remove
rule_list = []
for rule in vpn_rules['result']['entry']:
    for zone in rule['from']['member']:
        if f"{user_zone}" in zone.lower() or f"{user_zone}" in zone:
            rule_list.append(rule)

    for zone in rule['to']['member']:
        if f"{user_zone}" in zone.lower() or f"{user_zone}" in zone:
            rule_list.append(rule)

# This section begins to make the data payload from all of the key-value pairs of the rules in an exact one-for-one copy
# EXCEPT for the zone we want to remove, on a rule-by-rule basis. Each rule will have it's own entry in the list.
data_list = []
for rule in rule_list:
#    json.dump(rule, pre_zone_remove_outfile, indent=4)
#    pre_zone_remove_outfile.write("\n")

    # The payload template
    data = {}
    data['entry'] = {}

    # Iterates through all the key-value pairs and appends necessary values to the data payload
    for key, value in rule.items():
        # Omits the @device-group KVP because it's not needed
        if key == "@device-group":
            continue
        # Omits the @location KVP because it's not needed
        elif key == "@location":
            continue
        # Finds the source zone KVP and builds a new list that omits the zone we want to remove
        else:
            if key == "from" and "member" in value:
                zones = []

                for entry in value['member']:
                    if f"{user_zone}" in entry.lower() or f"{user_zone}" in entry:
                        continue
                    else:
                        zones.append(entry)

                # Adds the new zone list we built without the target zone
                if key == "from":
                    data['entry']['from'] = {}
                    data['entry']['from']['member'] = zones

            elif key == "to" and "member" in value:
                zones = []

                for entry in value['member']:
                    if f"{user_zone}" in entry.lower() or f"{user_zone}" in entry:
                        continue
                    else:
                        zones.append(entry)

                # Adds the new zone list we built without the target zone
                if key == "to":
                    data['entry']['to'] = {}
                    data['entry']['to']['member'] = zones

            # Builds the rest of the payload with all the same KVPs as the original rule
            else:
                data['entry'][f'{key}'] = value

    data_list.append(data)

# iterates through the rules in the list we made above and sends the payload
for rule in data_list:
    name = rule['entry']['@name']
#    old_rule_log.write(f'{name}\n')
#    json.dump(rule, post_zone_remove_outfile, indent=4)
#    post_zone_remove_outfile.write(",\n")

    # Prints the rule name that just got changed and status code of the API request response.
    pprint(f'Deleting zone from rule: {name}')

    # Specifies the payload
    data = rule

    # The actual API request that dynamically uses the rule name
    zone_update = requests.put(f'{base_url}/Policies/SecurityPostRules?name={name}&location=device-group&device-group={user_dg}',
                              headers=headers, verify=False, data=json.dumps(data))

    # We're looking for 200 here.
    pprint(zone_update)



