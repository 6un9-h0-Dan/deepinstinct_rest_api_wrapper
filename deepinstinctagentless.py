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

import requests, base64, json, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#define varibable for storing FQDN/IP of the agentless connector used for scan
agentless_connector = ''

def scan_file(file_name, encoded=False):
    # read file from disk. rb means opens the file in binary format for reading
    with open(file_name, 'rb') as f:
        #read file
        data = f.read()
        #close file
        f.close()

    if encoded:
        #encode file
        data = base64.b64encode(data)
        # set request url
        request_url = f'https://{agentless_connector}:5000/scan/base64'
    else:
        # set request url
        request_url = f'https://{agentless_connector}:5000/scan/binary'

    # send scan request, capture response
    response = requests.post(request_url, data=data, timeout=20, verify=False)

    if response.status_code == 200:
        verdict = response.json()
        return verdict
    else:
        print('ERROR: Unexpected return code', response.status_code,
        'on POST to', request_url)
        return None


def scan_file_encoded (file_name):
    return scan_file(encoded=True, file_name=file_name)
