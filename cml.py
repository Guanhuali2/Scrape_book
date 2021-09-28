import argparse


def command_line():
    """cml interface"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-scrape', type=str)
    parser.add_argument('-book_limit', type=int)
    parser.add_argument('-author_limit', type=int)
    parser.add_argument('-author_db', type=str)
    parser.add_argument('-book_db', type=str)
    parser.add_argument('-json_file', type=str)
    parser.add_argument('-json_command', type=int)
    parser.add_argument('-api_base', type=str)
    parser.add_argument('-method', type=str)
    parser.add_argument('-url', type=str)
    parser.add_argument('-parameters', type=str)
    args = parser.parse_args()
    start_url = args.scrape
    book_limit = args.book_limit
    author_limit = args.author_limit
    database1 = args.author_db
    database2 = args.book_db
    file_path = args.json_file
    command = args.json_command
    api_base = args.api_base
    method = args.method
    url = args.url
    parameters = args.parameters
    return start_url, author_limit, book_limit, database1, database2, file_path, command, \
           api_base, method, url, parameters
