import deepinstinct30 as di

di.fqdn = input('FQDN? ')
di.key = input('API Key? ')

print('INFO: Exporting devices')
di.export_devices()

print('INFO: Exporting policies')
di.export_policies(include_allow_deny_lists=True)

print('INFO: Exporting groups')
di.export_groups()

print('INFO: Exporting events')
minimum_event_id = input('First event ID to export (default 0)? ')
if minimum_event_id == '':
    minimum_event_id = 0
di.export_events(minimum_event_id=minimum_event_id)

print('INFO: Calling warranty_compliance_check.py')
exec(open('warranty_compliance_check.py').read())

print('INFO: Calling license_usage_report_by_tenant.py')
exec(open('license_usage_report_by_tenant.py').read())
