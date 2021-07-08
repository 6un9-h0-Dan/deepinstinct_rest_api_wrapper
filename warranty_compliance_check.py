import datetime

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
while di.fqdn in ('SERVER-NAME.customers.deepinstinctweb.com', ''):
    di.fqdn = input('FQDN of DI Server? ')
while di.key in ('API-KEY', ''):
    di.key = input('API Key? ')

#Get data from server
policies = di.get_policies(include_policy_data=True)

#Extract Windows policies
windows_policies = []
for policy in policies:
    if policy['os'] == 'WINDOWS':
        windows_policies.append(policy)

#Iterate through Windows policies, determine compliance or lack thereof, and assign to appropriate list

compliant_windows_policies = []
noncompliant_windows_policies = []

for policy in windows_policies:

    policy['compliant'] = True  #initially assume compliant; will change to false if violation(s) identified
    policy['compliance_violations'] = []  #define list to store details of violation(s) if any

    if policy['prevention_level'] not in ['HIGH', 'MEDIUM', 'LOW']:
        policy['compliant'] = False
        policy['compliance_violations'].append('prevention_level is set to ' + policy['prevention_level'])

    if policy['remote_code_injection'] != 'PREVENT':
        policy['compliant'] = False
        policy['compliance_violations'].append('remote_code_injection is set to ' + policy['remote_code_injection'])

    if policy['arbitrary_shellcode_execution'] != 'PREVENT':
        policy['compliant'] = False
        policy['compliance_violations'].append('arbitrary_shellcode_execution is set to ' + policy['arbitrary_shellcode_execution'])

    if policy['ransomware_behavior'] != 'PREVENT':
        policy['compliant'] = False
        policy['compliance_violations'].append('ransomware_behavior is set to ' + policy['ransomware_behavior'])

    #TODO: Add logic to check the following atttributes of the Windows policy:
    #   1. D-Cloud Services (compliance requires that this be enabled)
    #   2. Malicious PowerShell Prevention (compliance requires that this be in Prevention)
    #Both of above require that product make these fields visible via the REST API. Submitted
    #as FR-166 and FR-177 on 2021-07-06

    if policy['compliant'] == True:
        compliant_windows_policies.append(policy)
    else:
        noncompliant_windows_policies.append(policy)

#Print results to console

print('Deep Instinct Ransomware Warranty Compliance Check |', di.fqdn, '|', datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d_%H.%M"), 'UTC')

print('\nThe following Windows policies are compliant:')
print('compliant\tmsp_id\tmsp_name\tpolicy_id\tpolicy_name')
for policy in compliant_windows_policies:
    print(policy['compliant'], '\t', policy['msp_id'], '\t', policy['msp_name'], '\t', policy['id'], '\t', policy['name'])

print('\nThe following Windows policies are non-compliant:')
print('compliant\tmsp_id\tmsp_name\tpolicy_id\tpolicy_name\tcompliance_violations')
for policy in noncompliant_windows_policies:
    print(policy['compliant'], '\t', policy['msp_id'], '\t', policy['msp_name'], '\t', policy['id'], '\t', policy['name'], '\t', policy['compliance_violations'])
