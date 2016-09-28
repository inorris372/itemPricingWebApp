import re
import uuid
import requests
from bs4 import BeautifulSoup
from src.common.database import Database
from src.models.items import constants
from src.models.stores.store import Store


__author__ = 'Ian'


class Item(object):
    def __init__(self, name, url, _id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        tag_name = store.tag_name
        query = store.query
        self.price = self.load_item(tag_name, query)
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_item(self, tag_name, query):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(tag_name, query)
        string_price = element.txt.strip()

        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)

        return match.group()

    def save_to_mongo(self):
        Database.insert(constants.COLLECTION, self.json())
        pass

    def json(self):
        return {
            "name": self.name,
            "url": self.url
        }