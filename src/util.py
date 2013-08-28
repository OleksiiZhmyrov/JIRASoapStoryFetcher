import re
import sys
import datetime

import xlwt
import xlrd

from config import *
from jira import *


def estimation(seq):
    result = 0
    for item in seq:
        if item != '':
            result += int(float(str(item)))
    return result


def get_statistics(stories_list, epic):
    ba = []
    dev = []
    non_estimated = 0

    for issue in stories_list:

        # Story points are stored in GreenHopper, therefore JIRA SOAP API
        # does not have particular name for this field in responses. We have
        # to find required fields in the response as they do not have constant
        # index in the list.
        for index in range(5, 8):
            if issue[5][index].customfieldId in GREENHOPPER_CUSTOM_FIELDS:
                story_points = issue[5][index].values[0]
                break

        # Business Analysis stories have prefix 'BA:' but because of user's typos
        # it might be transformed to 'ba:', 'BA-', etc.
        p = re.compile('[Bb][Aa][: \-]', re.UNICODE)
        if p.match(issue.summary):
            ba.append(story_points)
        else:
            dev.append(story_points)
        if int(float(str(story_points))) == 0:
            non_estimated += 1

    return [epic[0], epic[1],
            len(ba), len(dev), len(ba) + len(dev),
            estimation(ba), estimation(dev),
            estimation(ba) + estimation(dev), non_estimated]


def get_results(auth):
    epics = get_epics(auth)
    result = []
    for epic in epics:
        stories_list = get_stories_from_epic(auth, epic)
        epic_statistics = get_statistics(stories_list, epic)
        result.append(epic_statistics)
    return result


def get_report_filename():
    now = datetime.datetime.now()
    return '../Stats_' + now.strftime("%Y.%m.%d_%H-%M-%S") + '.xls'


def get_cards_filename():
    now = datetime.datetime.now()
    return '../Cards_' + now.strftime("%Y.%m.%d_%H-%M-%S") + '.xls'

def get_sheet_name():
    now = datetime.datetime.now()
    sheet_name = now.strftime("%Y.%m.%d %H-%M-%S")
    return sheet_name


def add_header(sheet):
    header_style = xlwt.easyxf('font: bold on; pattern: pattern solid, fore_colour blue;')

    header_titles = ['Epic Key', 'Epic Summary',
                     'BA Count', 'DEV Count', 'Total Count',
                     'BA Est',   'DEV Est',   'Total Est',
                     'Unestimated']

    for col, value in enumerate(header_titles):
        sheet.col(col).width = 256 * (len(value) + 1)
        sheet.write(0, col, value, header_style)

    # Fix width of first and second column
    sheet.col(0).width = 256 * 15
    sheet.col(1).width = 256 * 30

    return sheet


def create_report(data):
    print 'Preparing report file...'

    report_file = xlwt.Workbook()
    sheet = report_file.add_sheet(get_sheet_name())
    sheet = add_header(sheet)

    compare_file = raw_input("File to compare with [none]: ")
    compare = False
    if compare_file not in ['none', '']:
        compare = True
        print 'Comparing...'
        previous_workbook = xlrd.open_workbook(compare_file)
        previous_sheet = previous_workbook.sheet_by_name(previous_workbook.sheet_names()[0])

    green_background = xlwt.easyxf('pattern: pattern solid, fore_colour green;')

    for row, epic in enumerate(data):
        for col, value in enumerate(epic):
            if compare:
                if value != previous_sheet.cell_value(row + 1, col):
                    sheet.write(row + 1, col, value, green_background)
                else:
                    sheet.write(row + 1, col, value)
            else:
                sheet.write(row + 1, col, value)

    filename = get_report_filename()
    report_file.save(filename)

    print 'Results saved in file: {file_name}'.format(file_name=filename)


def read_source_file():
    list = []
    fh = open(name=sys.argv[1], mode="r")
    for line in fh.readlines():
        if line is not None and line != "":
            list.append(line)
    return list


def render_cards(cards):
    out_file = xlwt.Workbook()
    sheet = out_file.add_sheet('test')

    for card in cards:
        sheet = card.render(sheet)

    filename = get_cards_filename()
    print 'Results saved in file: {file_name}'.format(file_name=filename)
    out_file.save(filename)

