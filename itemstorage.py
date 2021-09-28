"""class item"""


class ItemStorage():
    data = {
        "Author": [],
        "Book": []
    }

    def __init__(self, book_count, author_count):
        """initialize"""
        self.data["book_queue"] = []
        self.data["visited"] = []
        self.data["visited_author"] = []
        self.data["book_limit"] = book_count
        self.data["author_limit"] = author_count

    def pop_book(self):
        """pop book"""
        if len(self.data["book_queue"]) == 0:
            return None
        return self.data["book_queue"].pop(0)

    def pop_author(self):
        """pop author"""
        if len(self.data["author_queue"]) == 0:
            return None
        return self.data["author_queue"].pop(0)
