import getpass
import SOAPpy
from config import *
from classes import StoryCard
import re

soap = SOAPpy.WSDL.Proxy(JIRA_URL)


def authorize():
    jira_user = raw_input("Username for jira: ")
    if jira_user == '':
        print 'JIRA login can not be empty string.'
        exit()
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

        story_points = "n/a"
        epic_key = None
        tester = ""

        node = story[0][5]
        for i in range(1, len(node)+1):
            try:
                if node[i].customfieldId in GREENHOPPER_CUSTOM_FIELDS:
                    story_points = node[i].values[0]
                    continue
                elif node[i].customfieldId in EPIC_NAME_CUSTOM_FIELDS:
                    epic_key = node[i].values[0]
                    continue
                elif node[i].customfieldId in TESTER_CUSTOM_FIELDS:
                    tester = node[i].values[0]
                    continue
                else:
                    continue
            except IndexError:
                break

        if epic_key is not None:
            search_string = 'project = {project} AND issuetype = epic AND key = {key}'.format(
                project=PROJECT_NAME, key=epic_key)
            epic = soap.getIssuesFromJqlSearch(auth, search_string, SOAPpy.Types.intType(1))
            epic_summary = epic[0].summary
        else:
            epic_summary = "n/a"

        description = story[0].description
        description = (description, description[:127] + ' ...')[len(description) > 128]

        assignee = (re.sub('_', ' ', str(story[0].assignee)), '')[story[0].assignee is None]
        reporter = (re.sub('_', ' ', str(story[0].reporter)), '')[story[0].reporter is None]
        tester = re.sub('_', ' ', str(tester))

        result.append(
            StoryCard(
                index=index,
                number=story[0].key,
                summary=story[0].summary,
                description=description,
                assignee=assignee,
                tester=tester,
                reporter=reporter,
                points=story_points,
                epic=epic_summary
            )
        )
    return result

