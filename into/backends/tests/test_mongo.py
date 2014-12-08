import pymongo
from contextlib import contextmanager
import datashape
from into import discover, convert, append, resource
from into.backends.mongo import *
from toolz import pluck
from copy import deepcopy


conn = pymongo.MongoClient()
db = conn._test_db


@contextmanager
def coll(data):
    c = db.my_collection
    if data:
        c.insert(deepcopy(data))

    try:
        yield c
    finally:
        c.drop()

bank = ({'name': 'Alice', 'amount': 100},
        {'name': 'Alice', 'amount': 200},
        {'name': 'Bob', 'amount': 100},
        {'name': 'Bob', 'amount': 200},
        {'name': 'Bob', 'amount': 300})


dshape = datashape.dshape('var * {name: string, amount: int}')


def test_discover():
    with coll(bank) as c:
        assert discover(bank) == discover(c)


def test_append_convert():
    with coll([]) as c:
        append(c, bank, dshape=dshape)

        assert convert(list, c, dshape=dshape) == list(pluck(['name', 'amount'], bank))
