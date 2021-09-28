"""Json file"""
from json import load
from json import dump

def insert_database(file_path, d_a):
    try:
        with open(file_path) as json_file:
            import_data = load(json_file)
    except:
        print("invalid Json File/read")
        return
    for data in import_data["data"]:
        print(data)
        d_a.insert_one(data)

def insert_update_database(file_path, d_a, d_b):
    """ update database """
    try:
        with open(file_path) as json_file:
            import_data = load(json_file)
    except:
        print("invalid Json File/read")
        return

    for import_author in import_data["Author"]:
        try:
            author_id = import_author["author_id"]
        except KeyError:
            print("Json file does not have proper author id")
            return
        query = {"author_id": author_id}
        if d_a.find(query).count() > 0:
            d_a.update_one(query, {"$set": import_author})
            print("author " + author_id + " is updated")
        else:
            d_a.insert_one(import_author)
            print("author " + author_id + " is inserted")

    for import_book in import_data["Book"]:
        try:
            book_id = import_book["book_id"]
        except KeyError:
            print("Json file does not have proper book id")
            return
        query = {"book_id": book_id}
        if d_b.find(query).count() > 0:
            d_b.update_one(query, {"$set": import_book})
            print("book " + book_id + " is updated")
        else:
            d_b.insert_one(import_book)
            print("book " + book_id + " is inserted")


def write_to_json(path, data):
    """ write to json file"""
    try:
        with open(path, 'w') as outfile:
            dump(data, outfile)
    except:
        print("invalid Json path/write")
