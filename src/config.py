# Try to load constants from local settings file
try:
    from local_settings import *
except ImportError:
    pass

# JIRA_URL = 'https://www.atlassian.com/rpc/soap/jirasoapservice-v2?WSDL'
# GREENHOPPER_CUSTOM_FIELDS = ['customfield_10000', 'customfield_10001']
# EPIC_NAME_CUSTOM_FIELDS = ['customfield_10002']
# PROJECT_NAME = 'MYPROJECT'
# TARGET_EPICS = ['MYPROJECT-631', 'MYPROJECT-8734']

