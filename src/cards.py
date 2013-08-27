import xlwt
from util import *

list = []


def render_cards(cards):
    out_file = xlwt.Workbook()
    sheet = out_file.add_sheet('test')

    for card in cards:
        sheet = card.render(sheet)

    out_file.save('D:/test.xls')


if __name__ == "__main__":
    auth = authorize()
    cards = get_stories_from_list(auth, list)
    render_cards(cards)


