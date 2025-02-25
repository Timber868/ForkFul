from flask import Flask

from app import app

def before_feature(context, feature):
    context.app = app
    context.client = context.app.test_client()