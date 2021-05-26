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

# Prompt use for D-Appliance Version, validate input, then import appropriate
# version of the REST API Wrapper
di_version = ''
while di_version not in ['3.0', '2.5']:
    di_version = input('DI Server Version [3.0 | 2.5]? ')
if di_version == '3.0':
    import deepinstinct30 as di
else:
    import deepinstinct25 as di

# Optional hardcoded config - if not provided, you'll be prompted at runtime
di.fqdn = 'SERVER-NAME.customers.deepinstinctweb.com'
di.key = 'API-KEY'

# Validate config and prompt if not provided above
while di.fqdn == '' or di.fqdn == 'SERVER-NAME.customers.deepinstinctweb.com':
    di.fqdn = input('FQDN of DI Server? ')
while len(di.key) != 257:
    di.key = input('API Key? ')

#Prompt for Device Group Name
device_group_name = input('Device Group Name? ')

#Prompt for hostname(s)
device_name_list = []
device_name = None
while device_name != '':
    device_name = input('Enter hostname to add, or press enter to exit: ')
    if device_name != '':
        device_name_list.append(device_name)

#Print preview of the move to the console
print('\nDevice(s) with hostname(s)\n',device_name_list, '\nwill be moved to\n', device_group_name, '\non server\n', di.fqdn, '\nusing API key\n', di.key, '\n')

#Ask user to confirm
user_input = input('To execute the above change, type YES in all caps and press return: ')

#Check user response
if user_input == 'YES':
    print('\nSending request to server')
    #Call move_devices to execute the change
    result = di.move_devices(device_name_list, device_group_name)
    #Check results and print summary to console if successful
    if result != None:
        #change was sucessful. print details to console
        print(result)
    else:
        print('Something went wrong. No devices were moved.')
else:
    #User response did not approve the change
    print('The change was aborted.')
