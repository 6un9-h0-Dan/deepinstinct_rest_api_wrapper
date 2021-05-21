# deepinstinct-rest-api-wrapper

Deep Instinct REST API Wrapper

Compatibility:
* deepinstinct30 - Designed for and tested using Deep Instinct D-Appliance version 3.0.0.0
* deepinstinct25 - Designed for and tested using Deep Instinct D-Appliance version 2.5.0.1
* Written and tested using a Python 3.8.3 instance installed by Anaconda

Suggested Usage:

1. Save deepinstinct*.py in the same directory as your own code
2. Depending upon which version of the Deep Instinct server you are interacting with, include one of the following at the top of your code:
   import deepinstinct30 as di
   or
   import deepinstinct25 as di
3. Set/modify the DI server name like this: di.fqdn = 'SERVER-NAME'
4. Set/modify the DI REST API key like this: di.key = 'API-KEY'
5. Invoke the REST API methods like this:  di.function_name(arg1, arg2)
6. For testing and interactive usage, I use and recommend Jupyter Notebook, which is installed as part of Anaconda (https://www.anaconda.com/)
7. Reference the samples provided in this project (all files not matching deepinstinct*.py) for examples of how to import and use the API Wrapper as described above

Disclaimer:
All code in this project is provided as an example of how to build logic against and interact with the Deep Instinct REST API. It is provided AS-IS/NO WARRANTY. It has limited error checking and logging, and likely contains defects or other deficiencies. Test thoroughly first, and use at your own risk. This API Wrapper is not a Deep Instinct commercial product and is not officially supported, although the underlying REST API is. This means that to report an issue to tech support you must remove the API Wrapper layer and recreate the problem against the raw/pure DI REST API.
