from app.database import *

from app.models.map import *
from app.models.map.services.search import search

def check_search():
    print(search([p.name for p in Poi.all()], input()))