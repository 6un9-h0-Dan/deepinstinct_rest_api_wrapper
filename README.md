# deepinstinct-rest-api-wrapper

Deep Instinct v2.5 REST API Wrapper
Compatability:
-Designed for and tested using Deep Instinct D-Appliance version 2.5.0.1
-Written and tested using a Python 3.8.3 instance installed by Anaconda

Suggested Usage:
1. Save this file as deepinstinct25.py in the same directory as your code
2. Include "import deepinstinct25 as di" at the top of your code
3. Set/modify the DI server name like this: di.fqdn = 'SERVER-NAME'
4. Set/modify the DI REST API key like this: di.key = 'API-KEY'
5. Invoke the REST API methods like this:  di.function_name(arg1, arg2)
6. For testing and interactive usage, I use and recommend Jupyter Notebook, which is installed as part of Anaconda (https://www.anaconda.com/)

Disclaimer:
This code is provided as an example of how to build code against and interact with the Deep Instinct REST API. It is provided AS-IS/NO WARRANTY. It has limited error checking and logging, and likely contains defects or other deficiencies. Test thoroughly first, and use at your own risk. This API Wrapper is not a Deep Instinct commercial product and is not officially supported, althought he underlying REST API is. This means that to report an issue to tech support you must remove the API Wrapper layer and recreate the problem against the raw/pure DI REST API.
