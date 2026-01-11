from backend.database import dbread
from random import shuffle
import clotheselector
import getimages

def process(filters):
    data = dbread.query(filters)
    shuffle(data)

    top = clotheselector.select(data, 'top')
    pants = clotheselector.select(data, 'pants')
    overshirt = clotheselector.select(data, 'overshirt')

    outfit = [getimages.get(top), getimages.get(pants), getimages.get(overshirt)]

    return outfit
