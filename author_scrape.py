import requests
import re
from bs4 import BeautifulSoup as bs4


class author_scrape():
    """author scraping"""
    base_url = None
    page = None
    dict = {}
    url = ""

    def __init__(self, url, base):
        """initialize"""
        self.url = url
        self.dict = {
            "name": "",
            "author_url": "",
            "author_id": "",
            "rating": "",
            "rating_count": "",
            "review_count": "",
            "image_url": "",
            "related_authors": [],
            "author_books": [],
        }
        pattern = r"https://www.goodreads.com/author/show/\d+.[a-zA-Z\_]+"
        self.base_url = base
        if re.match(pattern, url):
            try:
                self.page = requests.get(url)
            except TypeError:
                print("invalid url")
                return
            pattern = r'\d+'
            self.dict["author_url"] = url
            try:
                self.dict["author_id"] = re.findall(pattern, url)[0]
            except IndexError:
                self.dict["author_id"] = "no id"
            self.scrape(self.page)
        else:
            print("invalid website")
            return

    def scrape(self, page):
        """main scraping"""
        soup = bs4(page.content, 'html.parser')
        self.get_author_name(soup)

        self.get_author_rating(soup)

        self.get_rating_count(soup)

        self.get_review_count(soup)

        self.get_author_image(soup)

        books = soup.select('a.bookTitle>span[itemprop="name"]')
        for book in books:
            self.dict["author_books"].append(book.text)
        try:
            text = soup.select('a:contains("Similar authors")')[0].get('href')
        except IndexError:
            print("no related author for this url: " + self.url)
            self.dict["related_authors"] = "no similar author"
            return

        try:
            new_page = requests.get(self.base_url + text)
            self.get_related(new_page)
        except IndexError:
            print("invalid related author url: " + self.url)
            return

    def get_author_image(self, soup):
        """author image"""
        try:
            self.dict["image_url"] = soup.select('div.leftContainer.authorLeftContainer>a>img[itemprop="image"]')[
                0].get('src')
        except IndexError:
            print("no image for this author: " + self.url)
            self.dict["image_url"] = "no image for this author"

    def get_review_count(self, soup):
        """review count"""
        try:
            self.dict["review_count"] = soup.select('span.value-title[itemprop="reviewCount"]')[0].text.strip()
        except IndexError:
            self.dict["review_count"] = "no review count"

    def get_rating_count(self, soup):
        """rating count"""
        try:
            self.dict["rating_count"] = soup.select('span.value-title[itemprop="ratingCount"]')[0].text.strip()
        except IndexError:
            self.dict["rating_count"] = "no rating count"

    def get_author_rating(self, soup):
        try:
            self.dict["rating"] = soup.select('span.average[itemprop="ratingValue"]')[0].text.strip()
        except IndexError:
            self.dict["rating"] = "no rating"

    def get_author_name(self, soup):
        """author name"""
        try:
            self.dict["name"] = soup.select("h1.authorName > span[itemprop='name']")[0].text
        except IndexError:
            self.dict["name"] = "no name"

    def get_related(self, page):
        """get related author"""
        soup = bs4(page.content, 'html.parser')
        authors = soup.select('span[itemprop="name"]')
        for a in authors:
            if a.text in self.dict["name"]:
                continue
            self.dict["related_authors"].append(a.text)
