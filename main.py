"""main file"""
import re
import sys
import pymongo
import Json
import itemstorage
import book_scrape
import cml
import requests

def delete_dict():
    """delete dictions"""
    del stored.data["visited"]
    del stored.data["book_limit"]
    del stored.data["author_limit"]
    del stored.data["visited_author"]
    del stored.data["book_queue"]


def initialize_database():
    """initialize database"""
    global DA, DB
    try:
        webclient = pymongo.MongoClient(
            "mongodb+srv://Guanhua:champion328@cluster0.fwffs.mongodb.net/"
            "myFirstDatabase?retryWrites=true&w=majority")
    except TypeError:
        print("database connect error")
        sys.exit(1)
    print("database connected")
    data = webclient.data
    DA = data[database1]
    DB = data[database2]


def scraping_loop():
    """loop for scraping"""
    author_search = True
    count = 0
    while not len(stored.data["book_queue"]) <= 0:
        if (len(stored.data["Book"]) >= stored.data["book_limit"]) \
                or (len(stored.data["Book"]) >= 1900):
            break
        url = stored.pop_book()
        if url not in stored.data["visited"]:
            count += 1
            print(url + " # " + str(count))
            dicts = book_scrape. \
                book_scrape(url, BASE_URL, stored.data["visited_author"], author_search)
        else:
            continue
        stored.data["visited"].append(url)
        DB.insert_one(dicts.dict.copy())
        stored.data["Book"].append(dicts.dict.copy())

        if author_search:
            for info in dicts.a_info:
                DA.insert_one(info.copy())
                stored.data["Author"].append(info.copy())
                stored.data["visited_author"].append(info["author_url"])

        for i in dicts.output:
            if i not in stored.data["visited"]:
                stored.data["book_queue"].append(i)

        if len(stored.data["Author"]) >= stored.data["author_limit"]:
            author_search = False


start_url, author_limit, book_limit, database1, database2, file_path, json_command, api_base, method, url, parameters \
    = cml.command_line()

if book_limit >= 200 or author_limit >= 50 or author_limit < 0 or book_limit < 0:
    print("amount warning!")

PATTERN = r"https://www.goodreads.com/book/show/\d+.[a-zA-Z\_]+"
if not re.match(PATTERN, start_url):
    sys.exit("invalid start url")

stored = itemstorage.ItemStorage(book_limit, author_limit)
BASE_URL = "https://www.goodreads.com"
stored.data["book_queue"].append(start_url)

initialize_database()
print(json_command)
if json_command:
    Json.insert_update_database(file_path, DA, DB)

scraping_loop()

delete_dict()

if stored.data:
    Json.write_to_json(file_path, stored.data)

if method == "GET":
    response = requests.get(api_base + url, parameters)
    print(response.json())
if method == "PUT":
    response = requests.put(api_base + url, parameters)
if method == "DELETE":
    response = requests.delete(api_base + url)
if method == "POST":
    response = requests.post(api_base + url, parameters)