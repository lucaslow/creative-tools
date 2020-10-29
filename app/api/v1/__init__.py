from flask import Blueprint

from app.api.v1.adjustImageTone import adjustImageTone


def configBluePrintV1():
    v1 = Blueprint('v1', __name__)
    adjustImageTone.register(v1)
    return v1