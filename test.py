import requests

BASE = "http://127.0.0.1:5000/"
#response = requests.post(BASE + "scrape?attr=author%2Fshow%2F5110.Cesar_Millan")
#response = requests.get(BASE + "search/author.rating: > 3.8")
#response = requests.post(BASE + "author", {"authors": "test.txt"})
#response = requests.put(BASE + "author/id%3A15670", {"name": "guanhua", "title": "li"})
response = requests.delete(BASE + "author/id%3A2815")
# response = requests.delete(BASE + "book/id%3A1234567")

# response = requests.put(BASE + "book/id%3A7546", {"title": "Guanhua"})
#response = requests.delete(BASE + "author/id%3A5110")
#response = requests.post(BASE + "author/id%3A2815")
#response = requests.get(BASE + "8/top-books")

print(response)
response.close()
