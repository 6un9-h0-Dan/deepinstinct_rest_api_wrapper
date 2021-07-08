import deepinstinct30 as di  #Import appropriate version of REST API Wrapper from https://github.com/pvz01/deepinstinct-rest-api-wrapper/ that matches D-Appliance version
import datetime
​
di.key = 'foo'   #Requires a REST API key with minimum Read Only privileges.
di.fqdn = 'bar'
​
#Get all available policy data
policies = di.get_policies(include_policy_data=True)
​
#Iterate through policies and determine compliance or lack thereof
for policy in policies:
    
    if policy['os'] == 'WINDOWS':
        
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
​
#Print results
​
print('Deep Instinct Ransomware Warranty Compliance Check |', di.fqdn, '|', datetime.datetime.today().strftime("%Y-%m-%d_%H.%M"))
​
print('\nThe following Windows policies ARE compliant:')
for policy in policies:
    if policy['os'] == 'WINDOWS':
        if policy['compliant']:
            print(policy['msp_id'], policy['id'], policy['name'])
​
print('\nThe following Windows policies ARE NOT compliant:')
for policy in policies:
    if policy['os'] == 'WINDOWS':
        if not policy['compliant']:
            print(policy['msp_id'], policy['id'], policy['name'], '\nViolations:',  policy['compliance_violations'], '\n')
    