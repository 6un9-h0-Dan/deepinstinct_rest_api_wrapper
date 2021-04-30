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

# ==============================================================================
# THIS SECTION SHOWS A SERIES OF EXAMPLES OF HOW TO USE di.get_events TO GET
# ALL OR SOME OF THE EVENTS VISIBLE TO THE PROVIDED API KEY FROM THE SERVER
# --> Leave exactly 1 call to di.get_events uncommented
# --> Reference the API documentation (https://fqdn/api/v1) for data on all
#     available fields and values for the event search

# Get all events (no filter)
events = di.get_events()  #all events

# Get only events with event id > 1000
#events = di.get_events(minimum_event_id=1001)

# Build a set of event search parameters, then use them along with a minimum
# event id to get only events that match all provided criteria
#search_parameters = {}
#search_parameters['status'] = ['OPEN']
#search_parameters['threat_severity'] = ['LOW', 'MODERATE']
#events = di.get_events(minimum_event_id=101, search=search_parameters)
# ==============================================================================

if len(events) > 0:
    # Convert event data to a Pandas data frame for easier manipulation and export
    events_df = pandas.DataFrame(events)
    # Sort the data frame by event id
    events_df.sort_values(by=['id'], inplace=True)
    # Export the data frame to disk in Excel format
    file_name = f'events_{di.fqdn}_{datetime.datetime.today().strftime("%Y-%m-%d_%H.%M")}.xlsx'
    events_df.to_excel(file_name, index=False)
    print('Data was exported to disk as', file_name)
else:
    print('No events were found on the server')
