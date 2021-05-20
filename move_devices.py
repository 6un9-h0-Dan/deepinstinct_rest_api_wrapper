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

import deepinstinct25 as di

#CONFIGURATION

#Server name and API key
di.fqdn = 'SERVER-NAME.customers.deepinstinctweb.com'
di.key= 'API-KEY'

#Name of Device Group to move the devices to
device_group_name = 'My Prevention Group'

#Build a Python list of the hostnames to move
device_list = []
device_list.append('hostname1')
device_list.append('hostname2')
device_list.append('hostname3')

#RUNTIME

#Print preview of the move to the console
print(device_list, '\nwill be moved to\n', device_group_name, '\non server\n', di.fqdn, '\nusing API key\n', di.key, '\n')

#Ask user to confirm
user_input = input('To execute the above change, type YES in all caps and press return ')

#Check user response
if user_input == 'YES':
    print('Sending request to server')
    #Call move_devices to execute the change
    result = di.move_devices(device_list, device_group_name)
    #Check results and print summary to console if successful
    if result != None:
        #change was sucessful. print details to console
        print(result)
    else:
        print('Something went wrong. No devices were moved.')
else:
    #User response did not approve the change
    print('The change was aborted.')
