# Disclaimer:
# This code is provided as an example of how to build code against and interact
# with the Deep Instinct REST API. It is provided AS-IS/NO WARRANTY. It has
# limited error checking and logging, and likely contains defects or other
# deficiencies. Test thoroughly first, and use at your own risk. The API
# Wrapper and associated samples are not Deep Instinct commercial products and
# are not officially supported, although he underlying REST API is. This means
# that to report an issue to tech support you must remove the API Wrapper layer
# and recreate the problem with a reproducible test case against the raw/pure
# DI REST API.
#

import deepinstinct25 as di, datetime

# Optional hardcoded config - if not provided, you'll be prompted at runtime
di.fqdn = 'SERVER-NAME.customers.deepinstinctweb.com'
di.key = 'API-KEY'

# Validate config and prompt if not provided above
while di.fqdn == '' or di.fqdn == 'SERVER-NAME.customers.deepinstinctweb.com':
    di.fqdn = input('FQDN of DI Server? ')
while len(di.key) != 257:
    di.key = input('API Key? ')

# Get device data from DI server
devices = di.get_devices()

# Get current time and store as variable
now = datetime.datetime.utcnow()

# Define a list to store devices which meet criteria to be removed
devices_to_remove = []

# Inspect device data and build list of devices to be removed
# In the nested for loops below, only devices which meet ALL criteria will be removed.
# You'll need to adjust this area of the code to match your specific use case(s).
# Open https://{fqdn}/api/v1/ in a web browser and reference the specification for
# the 'DeviceList' model to see all available fields and possible values.
for device in devices:
    if 'tag' in device:   #needed to avoid KeyError for devices with no tag
        if device['tag'] == 'Your VDI Device Tag': #substitute actual device tag that you use for VDI devices
            if device['group_name'] == 'Your VDI Device Group Name':  #substitute actual group name for your VDI devices
                if device['license_status'] == 'ACTIVATED': #only include devices consuming a license
                    if device['connectivity_status'] == 'OFFLINE': #only include offline devices
                        if device['deployment_status'] == 'REGISTERED': #filtering on registered avoids duplicate requests
                            #convert last_contact form server to a Python datetime object
                            last_contact = datetime.datetime.fromisoformat(device['last_contact'].replace('Z',''))
                            #check if device's last_contact is long enough ago to meet criteria
                            #you can customize the timedelta below (default 12 hours)
                            if (now - last_contact) > datetime.timedelta(hours=12):
                                #all criteria above were met, therefore adding current device to the removal list
                                devices_to_remove.append(device)

# Process the list of devices which were identified for removal
for device in devices_to_remove:
    print('Requesting removal of device', )
    removal_status = di.remove_device(device)
    if removal_status:
        print(device['id'], device['hostname'], 'was successfully removed')
    else:
        print('Failed to remove', device['id'], device['hostname'])
