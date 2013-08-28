from util import *

if __name__ == "__main__":
    list = read_source_file()
    auth = authorize()
    cards = get_stories_from_list(auth, list)
    render_cards(cards)

