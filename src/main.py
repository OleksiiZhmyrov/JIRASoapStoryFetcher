from util import *

if __name__ == "__main__":
    auth = authorize()
    data = get_results(auth)
    create_report(data)
