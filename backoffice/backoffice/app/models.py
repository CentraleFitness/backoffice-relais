"""
Definition of models.
"""

from pymongo import MongoClient

from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

validate_even = RegexValidator(r"^\w{4}([-]?\w{4}){3}", "La clé doit être de la forme 0000-0000-0000-0000 avec des caractères alphanumériques.")

# Model for API keys

class MongoClientHandler():
    def __init__(self, host: str='localhost', port: int=27017):
        self.client = MongoClient(host, port)

class MongoDB(MongoClientHandler):
    def __init__(self, db: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = self.client[db]

class MongoCollection(MongoDB):
    def __init__(self, collection: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collection = self.db[collection]
    
class apiKey(models.Model):
    api_key = models.CharField(max_length=19, validators=[validate_even])
    date_creation = models.DateTimeField(default=timezone.now)
    date_expiration = models.DateTimeField(default=timezone.now)

    def __str__(self):
         return self.api_key
