import unittest
import requests
import queryope


class TestQuery(unittest.TestCase):
    def testNormalValid(self):
        query = 'book.book_id: 43'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(find.count(), 3)

    def testNormalInValid(self):
        query = 'book.lalala: 43'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(find.count(), 0)

    def testNormalSpecific(self):
        query = 'book.book_id: "24326516"'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(find.count(), 1)

    def testAndValid(self):
        query = 'book.book_id: 3 AND book.isbn: 1'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(find.count(), 19)

    def testOrValid(self):
        query = 'book.book_id: 32 OR book.isbn: 13'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(find.count(), 5)

    def testNotValid(self):
        query = 'book.book_id: NOT 0'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(find.count(), 29)

    def testLtInvalid(self):
        query = 'book.title: < guanhua'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(find, None)

    def testGtInvalid(self):
        query = 'book.title: > guanhua'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(find, None)

    def testGtValid(self):
        query = 'book.rating: > 4.3'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(find.count(), 12)

    def testLtValid(self):
        query = 'book.rating: < 3.5'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(find.count(), 2)

class TestApi(unittest.TestCase):
    BASE = "http://127.0.0.1:5000/"

    def testGetBook(self):
        response = requests.get(self.BASE+"book/id%3A7546")
        query = 'book.book_id: 7546'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(list(find)[0]['title'], response.json()[0]['title'])

    def testGetAuthor(self):
        response = requests.get(self.BASE+"author/id%3A15670")
        query = 'author.author_id: 15670'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(list(find)[0]['name'], response.json()[0]['name'])

    def testGetSearch(self):
        response = requests.get(self.BASE+"search/author%2Erating%3A%20>%203.8")
        query = 'author.rating: > 3.8'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(find.count(), len(response.json()))

    def testPutAuthor(self):
        response = requests.put(self.BASE + "author/id%3A15670", {"name": "Guanhua"})
        query = 'author.author_id: 15670'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(list(find)[0]['name'], "Guanhua")
        requests.put(self.BASE + "author/id%3A15670", {"name": "Temple Grandin"})

    def testPutBook(self):
        response = requests.put(self.BASE + "book/id%3A7546", {"title": "Guanhua"})
        query = 'book.book_id: 7546'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(list(find)[0]['title'], "Guanhua")
        requests.put(self.BASE + "book/id%3A7546",
            {"title": "Cesar's Way: The Natural, Everyday Guide to Understanding and Correcting Common Dog Problems"})

    def testPostAuthor(self):
        response = requests.post(self.BASE + "author", {"authors": "post_author.txt"})
        query = 'author.author_id: 2815'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(find.count(), 1)
        requests.delete(self.BASE + "author/id%3A2815")

    def testDeleteAuthor(self):
        response = requests.delete(self.BASE + "author/id%3A2815")
        query = 'author.author_id: 2815'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(find.count(), 0)

    def testPostBook(self):
        response = requests.post(self.BASE + "book", {"books": "post_book.txt"})
        query = 'book.book_id: 1234567'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(find.count(), 1)
        requests.delete(self.BASE + "book/id%3A1234567")

    def testDeleteBook(self):
        response = requests.delete(self.BASE + "book/id%3A1234567")
        query = 'book.book_id: 1234567'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(find.count(), 0)

    def testPostScrape(self):
        requests.post(self.BASE + "scrape?attr=author%2Fshow%2F5110.Cesar_Millan")
        query = 'author.author_id: 5110'
        sen = queryope.QueryOpe(query)
        find = queryope.querySearch(sen)
        self.assertEqual(find.count(), 1)
        requests.delete(self.BASE + "author/id%3A5110")


if __name__ == '__main__':
    unittest.main()