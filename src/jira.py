import getpass
import SOAPpy
from config import *

soap = SOAPpy.WSDL.Proxy(JIRA_URL)


def authorize():
    jira_user = raw_input("Username for jira: ")
    if jira_user == "":
        print 'JIRA login can not be empty string.'
        exit
    password = getpass.getpass('Password for %s: (will not echo)' % jira_user)

    print 'Logging in to JIRA as {user}'.format(user=jira_user)
    auth = soap.login(jira_user, password)

    return auth


def get_epics(auth):
    print 'Fetching Epics from JIRA...'
    epics = []
    for epic in TARGET_EPICS:
        epics.append([epic, soap.getIssue(auth, epic).summary])
    return epics


def get_stories_from_epic(auth, epic):
    print '\tWorking with epic {epic_key} \"{epic_summary}\"'.format(
        epic_key=epic[0], epic_summary=epic[1])

    search_string = 'project = {project} AND issuetype = story AND "Epic Link" = {epic_link}'.format(
        project=PROJECT_NAME, epic_link=epic[0])

    stories_list = soap.getIssuesFromJqlSearch(auth, search_string, SOAPpy.Types.intType(3000))
    return stories_list
