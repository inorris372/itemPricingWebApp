import re
import uuid
import requests
from bs4 import BeautifulSoup
from src.common.database import Database
from src.models.items import constants as ItemConstants
from src.models.stores.store import Store


__author__ = 'Ian'


class Item(object):
    def __init__(self, name, url, price, _id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.txt.strip()

        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)
        self.price = float(match.group())
        return self.price

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {'_id': self._id}, self.json())
        pass

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url
        }

    @classmethod
    def get_by_id(cls, item_id):
        return Database.find_one(ItemConstants.COLLECTION, {"_id": item_id})
