import author_scrape
import requests
import re
from bs4 import BeautifulSoup as bs4


class book_scrape():
    """book scraping"""
    base_url = None
    page = None
    dict = {}
    output = []
    a_info = []
    visited_author = []
    author_search = True

    def __init__(self, url, base, visited_author, author_search):
        """initialize"""
        self.author_search = author_search
        self.visited_author = visited_author
        self.dict = {
            "book_url": "",
            "title": "",
            "book_id": "",
            "isbn": "",
            "author_url": [],
            "author": [],
            "rating": "",
            "rating_count": "",
            "review_count": "",
            "image_url": "",
            "similar_books": []
        }
        self.output = []
        self.a_info = []
        pattern = r"https://www.goodreads.com/book/show/\d+.[a-zA-Z\_]+"
        self.base_url = base
        if re.match(pattern, url):
            try:
                # print(1)
                self.page = requests.get(url)
                # print(2)
            except TypeError:
                print("invalid url: " + url)
                return
            pattern = r'\d+'
            self.dict["book_url"] = url
            try:
                self.dict["book_id"] = re.findall(pattern, url)[0]
            except TypeError:
                self.dict["book_id"] = "no book id"
            self.scrape(self.page)
        else:
            print("invalid format of website: " + url)
            return

    def scrape(self, page):
        """scraping"""
        soup = bs4(page.content, 'html.parser')
        self.get_book_title(soup)

        self.get_book_rating(soup)

        self.get_rating_count(soup)

        self.get_review_count(soup)

        self.get_image_url(soup)

        self.get_book_isbn(soup)

        authors = soup.select('a.authorName>span')
        if len(authors) == 0:
            self.dict["author"] = "no author"
        else:
            for author in authors:
                self.dict["author"].append(author.text)

        urls = soup.select('a.authorName')
        if len(urls) == 0:
            self.dict["author_url"] = "no authors"
        else:
            for author_url in urls:
                a_url = author_url.get('href')
                if (a_url not in self.visited_author) and (self.author_search is True):
                    new_author = author_scrape.author_scrape(author_url.get('href'), self.base_url)
                    self.a_info.append(new_author.dict)
                self.dict["author_url"].append(a_url)

        try:
            text = soup.select('a:contains("See similar books")')[0].get('href')
            # print(3)
            new_page = requests.get(text)
            # print(4)
            self.get_similar(new_page)
            self.get_more_books(new_page)
        except IndexError:
            self.dict["similar_books"] = "no similar book"
            self.output = []

    def get_book_isbn(self, soup):
        """book isbm"""
        try:
            self.dict["isbn"] = soup.select('meta[property = "books:isbn"]')[0].get('content')
        except IndexError:
            print("this book does not have isbn")
            self.dict["isbn"] = "no isbn"

    def get_image_url(self, soup):
        """image url"""
        try:
            self.dict["image_url"] = soup.select('div.bookCoverPrimary>a>img[id="coverImage"]')[0].get('src')
        except IndexError:
            print("this book does not have image")
            self.dict["image_url"] = "no image"

    def get_review_count(self, soup):
        """review count"""
        try:
            self.dict["review_count"] = soup.select('#bookMeta > a > meta[itemprop="reviewCount"]')[0].get('content')
        except IndexError:
            self.dict["review_count"] = "no review count"

    def get_rating_count(self, soup):
        """rating count"""
        try:
            self.dict["rating_count"] = soup.select('#bookMeta > a > meta[itemprop="ratingCount"]')[0].get('content')
        except IndexError:
            self.dict["rating_count"] = "no rating count"

    def get_book_rating(self, soup):
        """book rating"""
        try:
            self.dict["rating"] = soup.select('span[itemprop="ratingValue"]')[0].text.strip()
        except IndexError:
            self.dict["rating"] = "no rating"

    def get_book_title(self, soup):
        """book title"""
        try:
            self.dict["title"] = soup.select("#bookTitle")[0].text.strip()
        except IndexError:
            self.dict["title"] = "no title"

    def get_similar(self, page):
        """similar"""
        soup = bs4(page.content, 'html.parser')
        try:
            books = soup.select('a>span[itemprop="name"]')
        except IndexError:
            return
        for b in books:
            if b.text in self.dict["title"]:
                continue
            self.dict["similar_books"].append(b.text)

    def get_more_books(self, page):
        """more books"""
        soup = bs4(page.content, 'html.parser')
        try:
            books = soup.select('div>a[itemprop="url"]')
        except TypeError:
            return
        for b in books:
            self.output.append(self.base_url + b.get('href'))
