import re
import sys
import Json
import pymongo
import book_scrape
import author_scrape
from flask import Flask
from flask_restful import Api, Resource, reqparse, request
import queryope
import heapq

app = Flask(__name__)
api = Api(app)
put_parser = reqparse.RequestParser()
post_parser = reqparse.RequestParser()


def post_api_parser(insert_parser):
    insert_parser.add_argument('books', type=str)
    insert_parser.add_argument('authors', type=str)

def put_api_parser(update_parser):
    update_parser.add_argument('name', type=str)
    update_parser.add_argument('rating', type=str)
    update_parser.add_argument('review_count', type=str)
    update_parser.add_argument('rating_count', type=str)
    update_parser.add_argument('image_url', type=str)
    update_parser.add_argument('related_authors', action='append')
    update_parser.add_argument('author_books', action='append')
    update_parser.add_argument('isbn', type=str)
    update_parser.add_argument('author_url', action='append')
    update_parser.add_argument('author', action='append')
    update_parser.add_argument('title', type=str)
    update_parser.add_argument('similar_books', action='append')


put_api_parser(put_parser)
post_api_parser(post_parser)


class PostApi(Resource):
    def post(self, database):
        web = self.connect_to_db()
        if database == "book" or database == "books":
            args = post_parser.parse_args()
            Json.insert_database(args["books"], web.data["book"])
        if database == "author" or database == "authors":
            args = post_parser.parse_args()
            Json.insert_database(args["authors"], web.data["author"])
        if database == "scrape":
            url = request.args["attr"]

            if "book" in url:
                pattern = r"book/show/\d+.[a-zA-Z\_]+"
                if re.match(pattern, url):
                    dicts = book_scrape.book_scrape("https://www.goodreads.com/" + url, "https://www.goodreads.com", [], False)
                    web.data["book"].insert_one(dicts.dict)
                else:
                    return [], 400
            if "author" in url:
                pattern = r"author/show/\d+.[a-zA-Z\_]+"
                if re.match(pattern, url):
                    dicts = author_scrape.author_scrape("https://www.goodreads.com/" + url, "https://www.goodreads.com")
                    web.data["author"].insert_one(dicts.dict)
                else:
                    return [], 400
        return 200

    def connect_to_db(self):
        try:
            webclient = pymongo.MongoClient(
                "mongodb+srv://Guanhua:champion328@cluster0.fwffs.mongodb.net/"
                "myFirstDatabase?retryWrites=true&w=majority")
        except TypeError:
            print("database connect error")
            sys.exit(1)
        return webclient

class QueryApi(Resource):
    def get(self, database, value):
        result = []
        if database == "author":
            if "id" not in value:
                return 400
            query = "author.author_" + value
            sen = queryope.QueryOpe(query)
            output = queryope.querySearch(sen)
            if output.count() < 1:
                print("no such file existed")
            for i in output:
                if i['_id']:
                    del i['_id']
                result.append(i)
        if database == "book":
            if "id" not in value:
                return 400
            query = "book.book_" + value
            sen = queryope.QueryOpe(query)
            output = queryope.querySearch(sen)
            if output.count() < 1:
                print("no such file existed")
            for i in output:
                if i['_id']:
                    del i['_id']
                result.append(i)
        if database == "search":
            query = value
            sen = queryope.QueryOpe(query)
            output = queryope.querySearch(sen)
            if output.count() < 1:
                print("no such file existed")
            for i in output:
                if i['_id']:
                    del i['_id']
                result.append(i)
        print(result)
        return result, 200

    def put(self, database, value):
        webclient = self.connect_to_db()
        try:
            args = put_parser.parse_args()
        except TypeError:
            print("wrong format of parameters")
            return [], 415
        db = webclient.data[database]
        if database == "book":
            query = "book.book_" + value
            sen = queryope.QueryOpe(query)
        if database == "author":
            query = "author.author_" + value
            sen = queryope.QueryOpe(query)

        if db.find({sen.field: sen.command}).count() < 1:
            print("no such id exist")
            return [], 400
        print(args)
        for arg in args:
            try:
                if args[arg] is not None:
                    db.update_many({sen.field: sen.command}, {"$set": {arg: args[arg]}})
            except KeyError:
                return 415
        return 200

    def connect_to_db(self):
        try:
            webclient = pymongo.MongoClient(
                "mongodb+srv://Guanhua:champion328@cluster0.fwffs.mongodb.net/"
                "myFirstDatabase?retryWrites=true&w=majority")
        except TypeError:
            print("database connect error")
            sys.exit(1)
        return webclient

    def delete(self, database, value):
        webclient = self.connect_to_db()
        db = webclient.data[database]
        if database == "author":
            query = "author.author_" + value
            sen = queryope.QueryOpe(query)
        if database == "book":
            query = "book.book_" + value
            sen = queryope.QueryOpe(query)
        d = db.delete_many({sen.field: sen.command})
        if d.deleted_count < 1:
            print(d.deleted_count)
            return [], 400
        return 200

class TopApi(Resource):
    def connect_to_db(self):
        try:
            webclient = pymongo.MongoClient(
                "mongodb+srv://Guanhua:champion328@cluster0.fwffs.mongodb.net/"
                "myFirstDatabase?retryWrites=true&w=majority")
        except TypeError:
            print("database connect error")
            sys.exit(1)
        return webclient

    def get(self, number, database):
        webclient = self.connect_to_db()
        if "author" in database:
            db = webclient.data["author"]
        if "book" in database:
            db = webclient.data["book"]
        collection = db.find({})
        results = []
        temp = []
        for documents in collection:
            del documents['_id']
            results.append(documents['rating'])
            temp.append(documents)
        mini = heapq.nlargest(number, results)
        output = []
        for documents in temp:
            if documents["rating"] in mini:
                output.append(documents)
        return sorted(output, key=lambda i: i['rating'], reverse=True)

api.add_resource(TopApi, '/<int:number>/<string:database>')
api.add_resource(QueryApi, '/<string:database>/<string:value>')
api.add_resource(PostApi, '/<string:database>')

if __name__ == '__main__':
    app.run(debug=True)
