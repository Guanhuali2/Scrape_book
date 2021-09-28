import sys
import re
import pymongo


class QueryOpe:
    valid = True
    object = None
    field = None
    specific = None
    command = None
    operator = None

    # check if the query valid or not
    def __init__(self, query):
        if "." not in query or ":" not in query:
            print("invalid query format")
            self.valid = False

        if "AND" in query:
            self.and_split(query)
        elif "OR" in query:
            self.or_split(query)
        else:
            self.normal_split(query)

    def normal_split(self, query):
        dian = query.split(".", 1)
        self.object = dian[0]
        # get query object
        maohao = dian[1].split(":")
        self.field = maohao[0]
        # get query field
        queries = maohao[1].strip().split(" ")
        if len(queries) > 1:
            self.operator = queries[0]
            # get query operator
            temp = queries[1]
        else:
            self.operator = None
            temp = queries[0]
        if temp[0] != '"' and temp[-1] != '"':
            self.specific = False
            # check query wants specific command or not
            self.command = temp
            # main query command
        elif temp[0] == '"' and temp[-1] == '"':
            self.specific = True
            self.command = temp.replace('"', '')
        else:
            print("quotes are not enclosed properly")
            self.valid = False

    def or_split(self, query):
        self.field = []
        self.specific = []
        self.command = []
        self.operator = "OR"
        two_part = query.split("OR")
        for x in two_part:
            x = x.strip()
            dian = x.split(".", 1)
            self.object = dian[0]
            # get query object
            maohao = dian[1].split(":")
            self.field.append(maohao[0])
            # get query field
            temp = maohao[1].strip()
            if temp[0] != '"' and temp[-1] != '"':
                self.specific.append(False)
                # check query wants specific command or not
                self.command.append(temp)
                # main query command
            elif temp[0] == '"' and temp[-1] == '"':
                self.specific.append(True)
                self.command.append(temp.replace('"', ''))
            else:
                print("quotes are not enclosed properly")
                self.valid = False

    def and_split(self, query):
        self.field = []
        self.specific = []
        self.command = []
        self.operator = "AND"
        two_part = query.split("AND")
        for x in two_part:
            x = x.strip()
            dian = x.split(".", 1)
            self.object = dian[0]
            # get query object
            maohao = dian[1].split(":")
            self.field.append(maohao[0])
            # get query field
            temp = maohao[1].strip()
            if temp[0] != '"' and temp[-1] != '"':
                self.specific.append(False)
                # check query wants specific command or not
                self.command.append(temp)
                # main query command
            elif temp[0] == '"' and temp[-1] == '"':
                self.specific.append(True)
                self.command.append(temp.replace('"', ''))
            else:
                print("quotes are not enclosed properly")
                self.valid = False


def noOpeSearch(collection, given_input):
    string = '{}'.format(given_input.command)
    if given_input.specific:
        sentence = {given_input.field: string}
    else:
        sentence = {given_input.field: {"$regex": string}}
    find = collection.find(sentence)
    if find.count() < 1:
        print("no such file existed")
    return find


def opeNot(collection, given_input):
    string = '{}'.format(given_input.command)
    if given_input.specific:
        sentence = {given_input.field: {"$not": string}}
    else:
        sentence = {given_input.field: {"$not": {"$regex": string}}}

    find = collection.find(sentence)
    if find.count() < 1:
        print("no such file existed")
    return find


def opeAnd(collection, given_input):
    list_query = []
    for i in range(len(given_input.command)):
        string = '{}'.format(given_input.command[i])
        if given_input.specific[i]:
            sentence = {given_input.field[i]: string}
        else:
            sentence = {given_input.field[i]: {"$regex": string}}
        list_query.append(sentence)
    find = collection.find({"$and": list_query})
    if find.count() < 1:
        print("no such file existed")
    return find


def opeOr(collection, given_input):
    list_query = []
    for i in range(len(given_input.command)):
        string = '{}'.format(given_input.command[i])
        if given_input.specific[i]:
            sentence = {given_input.field[i]: string}
        else:
            sentence = {given_input.field[i]: {"$regex": string}}
        list_query.append(sentence)
    find = collection.find({"$or": list_query})
    if find.count() < 1:
        print("no such file existed")
    return find


def opeLt(collection, given_input):
    pattern = r"\d+.{0,1}\d*"
    if re.match(pattern, given_input.command) and not given_input.specific:
        string = '{}'.format(given_input.command)
        sentence = {given_input.field: {"$lt": string}}
        return collection.find(sentence)
    else:
        print("comparison not between number")
        return


def opeGt(collection, given_input):
    pattern = r"\d+.{0,1}\d*"
    if re.match(pattern, given_input.command) and not given_input.specific:
        string = '{}'.format(given_input.command)
        sentence = {given_input.field: {"$gt": string}}
        return collection.find(sentence)
    else:
        print("comparison not between number")
        return


def querySearch(given_input):
    if not given_input.valid:
        return
    try:
        webclient = pymongo.MongoClient(
            "mongodb+srv://Guanhua:champion328@cluster0.fwffs.mongodb.net/"
            "myFirstDatabase?retryWrites=true&w=majority")
    except TypeError:
        print("database connect error")
        return
    data = webclient.data
    collection = data[given_input.object]

    if given_input.operator is None:
        return noOpeSearch(collection, given_input)
    if given_input.operator == "AND":
        return opeAnd(collection, given_input)
    if given_input.operator == "OR":
        return opeOr(collection, given_input)
    if given_input.operator == "NOT":
        return opeNot(collection, given_input)
    if given_input.operator == "<":
        return opeLt(collection, given_input)
    if given_input.operator == ">":
        return opeGt(collection, given_input)


# query = 'book.book_id: 373 OR book.isbn: 013'
# # query = 'book.rating: < 3.9'
# # query = 'book.rating: "3.87"'
# query = 'book.book_id: NOT 0'
# query = 'book.title: < guanhua'
# sen = QueryOpe(query)
# print(sen.valid, sen.object, sen.field, sen.specific, sen.operator, sen.command)
# find = querySearch(sen)
# for i in find:
#     print(i)
