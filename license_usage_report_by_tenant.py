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

import deepinstinct25 as di, pandas, datetime

# Optional hardcoded config - if not provided, you'll be prompted at runtime
di.fqdn = 'SERVER-NAME.customers.deepinstinctweb.com'
di.key = 'API-KEY'

# Validate config and prompt if not provided above
while di.fqdn == '' or di.fqdn == 'SERVER-NAME.customers.deepinstinctweb.com':
    di.fqdn = input('FQDN of DI Server? ')
while len(di.key) != 257:
    di.key = input('API Key? ')

# Get tenants, msps, and devices from DI server
tenants = di.get_tenants()
msps = di.get_msps()
devices = di.get_devices()

# Look up MSP name for each tenant and add it to the tenants data
for tenant in tenants:
    for msp in msps:
        if tenant['msp_id'] == msp['id']:
            tenant['msp_name'] = msp['name']

# Add licenses_used to tenants data with initial value 0
for tenant in tenants:
    tenant['licenses_used'] = 0

# Inspect each device in devices data
for device in devices:
    # Check if the device has an activated license (if not skip it)
    if device['license_status'] == 'ACTIVATED':
        # If yes, then find the Tenant that this device belongs to
        for tenant in tenants:
            if tenant['id'] == device['tenant_id']:
                # ...and increment the licenses_used counter in the matching tenant by 1
                tenant['licenses_used'] += 1

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
tenants_df.to_excel(file_name, index=False, columns=['msp_name', 'name', 'licenses_used', 'license_limit', 'percent_of_licenses_used'])
print('Data was exported to disk as', file_name)
