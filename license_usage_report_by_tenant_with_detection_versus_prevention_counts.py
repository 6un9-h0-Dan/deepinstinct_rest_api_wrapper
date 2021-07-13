print('INFO: Importing required libraries')
import deepinstinct30 as di, pandas, datetime

print('INFO: Setting config')
di.fqdn = 'foo'
di.key = 'bar'

print('INFO: Getting MSP data from server')
msps = di.get_msps()

print('INFO: Getting Tenant data from server')
tenants = di.get_tenants()

print('INFO: Adding MSP names to Tenant data')
for tenant in tenants:
    for msp in msps:
        if tenant['msp_id'] == msp['id']:
            tenant['msp_name'] = msp['name']

print('INFO: Getting Policy data from server')
policies = di.get_policies(include_policy_data=True)
print('INFO:', len(policies), 'policies returned')
 
print('INFO: Getting Device data from server')
devices = di.get_devices(include_deactivated=False)
print('INFO:', len(devices), 'devices returned')

print('INFO: Calculating and adding prevention_mode to devices (Windows only)')
prevention_count = 0
detection_count = 0
for device in devices:
    if device['os'] == 'WINDOWS':
        for policy in policies:
            if policy['id'] == device['policy_id']:
                if policy['prevention_level'] == 'DISABLED':
                    device['prevention_mode'] = False
                elif policy['ransomware_behavior'] != 'PREVENT':
                    device['prevention_mode'] = False
                elif policy['in_memory_protection'] != True:
                    device['prevention_mode'] = False
                elif policy['remote_code_injection'] != 'PREVENT':
                    device['prevention_mode'] = False
                elif policy['known_payload_execution'] != 'PREVENT':
                    device['prevention_mode'] = False
                elif policy['arbitrary_shellcode_execution'] != 'PREVENT':
                    device['prevention_mode'] = False
                else:
                    device['prevention_mode'] = True
        if device['prevention_mode']:
            prevention_count += 1
        else:
            detection_count += 1

print('INFO: Found', prevention_count, 'Windows devices in prevention')
print('INFO: Found', detection_count, 'Windows devices in detection')

print('INFO: Calculating licenses used and prevention/detection counts for each tenant')
for tenant in tenants:
    tenant['licenses_used'] = 0
    tenant['windows_devices_in_prevention'] = 0
    tenant['windows_devices_in_detection'] = 0
    for device in devices:
        if device['tenant_id'] == tenant['id']:
            tenant['licenses_used'] += 1
            if device['os'] == 'WINDOWS':
                if device['prevention_mode']:
                    tenant['windows_devices_in_prevention'] += 1
                else:
                    tenant['windows_devices_in_detection'] += 1

# Calculate percent_of_licenses_used for reach tenant and add results to tenants data
for tenant in tenants:
    if tenant['license_limit'] > 0:  #avoids a divisiion by zero error for tenants with no assigned licenses
        tenant['percent_of_licenses_used'] = (tenant['licenses_used'] / tenant['license_limit'] * 100)
    else:
        tenant['percent_of_licenses_used'] = 0

# Convert tenants data to a Pandas data frame for easier manipulation and export
tenants_df = pandas.DataFrame(tenants)

# Sort the data frame alphabetically by msp name and then by tenant name
tenants_df.sort_values(by=['msp_name', 'name'], inplace=True)

# Export the data frame to disk in Excel format
file_name = f'license_usage_report_by_tenant_{di.fqdn}_{datetime.datetime.today().strftime("%Y-%m-%d_%H.%M")}.xlsx'
tenants_df.to_excel(file_name, index=False, columns=['msp_name', 'name', 'licenses_used', 'license_limit', 'percent_of_licenses_used', 'windows_devices_in_prevention', 'windows_devices_in_detection'])
print('Data was exported to disk as', file_name)
