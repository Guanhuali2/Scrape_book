import json
import unittest
import pymongo
import itemstorage
import Json
import queryope


# class TestJson(unittest.TestCase):
#     Webclient = pymongo.MongoClient(
#         "mongodb+srv://Guanhua:champion328@cluster0.fwffs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#
#     def testInvalidJson(self):
#         data = self.Webclient.data
#         d_a = data["test_author"]
#         d_b = data["test_book"]
#         Json.insert_update_database("testInvalidFile.txt", d_a, d_b)
#         self.assertEqual(d_a.find({"author_id": "1567"}).count(), 0)
#
#     def testValidJson(self):
#         data = self.Webclient.data
#         d_a = data["test_author"]
#         d_b = data["test_book"]
#         Json.insert_update_database("data.txt", d_a, d_b)
        # self.assertEqual(d_a.find({"author_id": "5110"}).count(), 1)

    # def testValidJsonAuthorInsert(self):
    #     data = self.Webclient.data
    #     d_a = data["test_author"]
    #     d_b = data["test_book"]
    #     Json.insert_update_database("testReadableFileInsert.txt", d_a, d_b)
    #     dicts = d_a.find_one({"author_id": "1567"})
    #     self.assertEqual(dicts["author_id"], "1567")
    #     d_a.remove()
    #     d_b.remove()
    #
    # def testValidJsonAuthorUpdate(self):
    #     data = self.Webclient.data
    #     d_a = data["test_author"]
    #     d_b = data["test_book"]
    #     Json.insert_update_database("testReadableFileInsert.txt", d_a, d_b)
    #     Json.insert_update_database("testReadableFileUpdate.txt", d_a, d_b)
    #     dicts = d_a.find_one({"author_id": "1567"})
    #     self.assertEqual(dicts["name"], "Guanhua Li")
    #     d_a.remove()
    #     d_b.remove()
    #
    # def testValidJsonBookInsert(self):
    #     data = self.Webclient.data
    #     d_a = data["test_author"]
    #     d_b = data["test_book"]
    #     Json.insert_update_database("testReadableFileInsert.txt", d_a, d_b)
    #     dicts = d_b.find_one({"book_id": "31054"})
    #     self.assertEqual(dicts["book_id"], "31054")
    #     d_a.remove()
    #     d_b.remove()
    #
    # def testValidJsonBookUpdate(self):
    #     data = self.Webclient.data
    #     d_a = data["test_author"]
    #     d_b = data["test_book"]
    #     Json.insert_update_database("testReadableFileInsert.txt", d_a, d_b)
    #     Json.insert_update_database("testReadableFileUpdate.txt", d_a, d_b)
    #     dicts = d_b.find_one({"book_id": "31054"})
    #     self.assertEqual(dicts["title"], "Guanhua Li")
    #     d_a.remove()
    #     d_b.remove()

    # def testInValidJsonWrite(self):
    #     try:
    #         Json.write_to_json("testWriteInValid.txt", {"author": "Guanhua"})
    #     except:
    #         print("invalid")
    #
    # def testValidJsonWrite(self):
    #     Json.write_to_json("testWriteValid.txt", {"author": "Guanhua"})
    #     with open("testWriteValid.txt") as json_file:
    #         import_data = json.load(json_file)
    #     self.assertEqual(import_data["author"], "Guanhua")


# class TestCommandLine(unittest.TestCase):
#     def testInvalidCommandLineArguments(self):
#         start_url = cml.command_line()
#         print(start_url)
#         self.assertEqual(start_url, (None, None, None, None, None, None))


class TestItem(unittest.TestCase):
    def testInitializeItem(self):
        item = itemstorage.ItemStorage(1, 2)
        self.assertEqual(item.data["book_limit"], 1)
        self.assertEqual(item.data["author_limit"], 2)




if __name__ == '__main__':
    unittest.main()
