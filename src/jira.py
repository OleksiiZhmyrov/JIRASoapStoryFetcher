import getpass
import SOAPpy
from config import *
from classes import StoryCard

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


def get_stories_from_list(auth, list):
    result = []
    for index, story_number in enumerate(list):
        search_string = 'project = {project} AND issuetype = story AND key = {key}'.format(
            project=PROJECT_NAME, key=story_number)
        story = soap.getIssuesFromJqlSearch(auth, search_string, SOAPpy.Types.intType(1))

        story_points = 'n/a'
        for i in range(5, 8):
            if story[0][5][i].customfieldId in GREENHOPPER_CUSTOM_FIELDS:
                story_points = story[0][5][i].values[0]
                break

        for i in range(1, 5):
            if story[0][5][i].customfieldId in EPIC_NAME_CUSTOM_FIELDS:
                epic_key = story[0][5][i].values[0]
                break

        search_string = 'project = {project} AND issuetype = epic AND key = {key}'.format(
            project=PROJECT_NAME, key=epic_key)
        epic = soap.getIssuesFromJqlSearch(auth, search_string, SOAPpy.Types.intType(1))

        description = story[0].description
        description = (description, description[:128] + ' ...')[len(description) > 128]

        result.append(
            StoryCard(
                index=index,
                number=story[0].key,
                summary=story[0].summary,
                description=description,
                assignee=story[0].assignee,
                tester="TBD",
                reporter=story[0].reporter,
                points=story_points,
                epic=epic[0].summary
            )
        )
    return result

