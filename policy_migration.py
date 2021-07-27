# This is an example of how to copy policy data from one D-Appliance to another.
# In the case of multi-tenancy, it can also be used to copy policy data from one
# MSP to another on the same server.
#
# Known limitations:
# 1. The platform-specific default policies (example: Windows Default Policy) are not migrated
# 2. D-Appliance is sensitive to policy name collission. In the event of name collission, the policy is not migrated.
# 3. Only the policy settings that are available to read and write via the REST API are migrated. As of July 2021 there are
#    some exceptions such as D-Cloud Services and AMSI-based PowerShell features such as Malicious PowerShell Prevention.
#    Those settings are therefore not migrated and will remain at whatever value the destination server has set in the
#    default policies pre-migration.

# Configuration
source_fqdn = 'FOO.customers.deepinstinctweb.com'
source_key = 'api_key_for_foo'
destination_fqdn = 'BAR.customers.deepinstinctweb.com'
destination_key = 'api_key_for_bar'
platforms_to_migrate = ['MAC', 'WINDOWS']

#import REST API Wrapper for appropriate version of A-Appliance here
import deepinstinct30 as di, requests

#get policies from source server
print('INFO: Getting policies from source server', source_fqdn)
di.fqdn = source_fqdn
di.key = source_key
source_server_policies = di.get_policies(include_policy_data=True, keep_data_encapsulated=True)

#get policies from destination server
print('INFO: Getting policies from destination server', destination_fqdn)
di.fqdn = destination_fqdn
di.key = destination_key
destination_server_policies = di.get_policies(include_policy_data=True, keep_data_encapsulated=True)

#build a list of policy names from destination server
destination_server_policy_names = []
for policy in destination_server_policies:
    destination_server_policy_names.append(policy['name'])

#build a list of policies to migrate
print('INFO: Examining data to calculate which policies to migrate')
policies_to_migrate = []
for policy in source_server_policies:
    if policy['os'] in platforms_to_migrate:
        if not policy['is_default_policy']:
            if policy['name'] not in destination_server_policy_names:
                policies_to_migrate.append(policy)

#build dictionary of default policy IDs on destination server
print('INFO: Building dictionary of default policy IDs by platform on', destination_fqdn)
destination_default_policy_ids = {}
for policy in destination_server_policies:
    if policy['is_default_policy']:
        destination_default_policy_ids[policy['os']] = policy['id']

#migrate the policies
print('INFO: Prep work is done. Beginning to migrate data from', source_fqdn, 'to', destination_fqdn)
for policy in policies_to_migrate:

    #first step is to create the base policy, which we'll base on the platform-specific default policy
    print('INFO: Beginning migration of', policy['id'], policy['os'], policy['name'])
    new_policy = di.create_policy(policy['name'], destination_default_policy_ids[policy['os']])
    print('INFO: New policy is', new_policy['id'], policy['os'], new_policy['name'])

    #next step is to overwrite the policy data on the newly-create policy with data from old server
    print('INFO: Overwriting policy data to match source server config')
    new_policy_id = new_policy['id']
    request_url = f'https://{di.fqdn}/api/v1/policies/{new_policy_id}/data'
    headers = {'accept': 'application/json', 'Authorization': di.key}
    payload = {'data': policy['data']}
    response = requests.put(request_url, json=payload, headers=headers)
    if response.status_code == 204:
        print('INFO: Successfully overwrote policy data on', policy['id'], policy['os'], policy['name'])
    else:
        print('ERROR: Unexpected response', response.status_code, 'on PUT to', request_url)

print('Done migrating', len(policies_to_migrate), 'policies from', source_fqdn, 'to', destination_fqdn)
