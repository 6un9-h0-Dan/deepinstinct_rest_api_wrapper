# Disclaimer:
# This code is provided as an example of how to build code against and interact
# with the Deep Instinct Agentless Connector over REST API. It is provided
# AS-IS/NO WARRANTY. It has limited error checking and logging, and likely 
# contains defects or other deficiencies. Test thoroughly first, and use at your 
# own risk. This sample is not a Deep Instinct commercial product and is not
# officially supported, although the API that it calls is.
#

import requests, base64, json, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#varibable for storing FQDN/IP of the agentless connector for performing scan
agentless_connector = ''


def scan_file(file_name, encoded=False):
    # read file from disk. rb means opens the file in binary format for reading
    with open(file_name, 'rb') as f:
        #read file
        data = f.read()
        #close file
        f.close()

    if encoded:
        #encode data and set URL to match
        data = base64.b64encode(data)
        request_url = f'https://{agentless_connector}:5000/scan/base64'
    else:
        #leave data as-is and set URL to match
        request_url = f'https://{agentless_connector}:5000/scan/binary'

    # send scan request, capture response
    response = requests.post(request_url, data=data, timeout=20, verify=False)

    # validate response code, return verdict as Python dictionary
    if response.status_code == 200:
        verdict = response.json()
        return verdict
    else:
        print('ERROR: Unexpected return code', response.status_code,
        'on POST to', request_url)
        return None


def scan_file_encoded(file_name):
    return scan_file(encoded=True, file_name=file_name)
