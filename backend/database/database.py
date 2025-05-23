import sqlite3
from flask import g

DATABASE = 'database/database.db'
DATABASE_TEST = 'tests/test_database.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = lambda C, R: { c[0]: R[i] for i, c in enumerate(C.description) }  # Allows access to columns by name
    return g.db

def get_testing_db():
    if 'test_db' not in g:
        g.db = sqlite3.connect(DATABASE_TEST)
        g.db.row_factory = lambda C, R: { c[0]: R[i] for i, c in enumerate(C.description) }  # Allows access to columns by name
    return g.db