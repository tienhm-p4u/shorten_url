from hashids import Hashids
from flask import Blueprint, request, jsonify, current_app

import models
from lib.url_validate import is_valid_url
from lib import error

api = Blueprint(__name__, "url")


@api.route("/url", methods=["POST"])
def encode_url():
    url = request.values.get("url")

    if not is_valid_url(url):
        raise error.InvalidURL(url)

    existed = models.URL.find_by_url(url)
    if existed:
        url_id = existed.id
    else:
        created = models.URL.create({"url": url})
        url_id = created.id

    hashid = Hashids().encode(url_id)
    short_url = "http://%s%s" % (current_app.config["SHORTEN_PREFIX"], hashid)

    return jsonify({"shorten_url": short_url})


@api.route("/url/<hashid>", methods=["GET"])
def decode_url(hashid):
    item_id = Hashids().decode(hashid)
    if not item_id:
        raise error.NotFound(hashid)

    saved_url = models.URL.find_by_id(item_id)
    if not saved_url:
        raise error.NotFound(hashid)

    return jsonify({"url": saved_url.url})


@api.errorhandler(error.BaseError)
def handle_error(e: error.BaseError):
    """
    Handle known error
    :param e: error
    :return: response
    """
    # TODO: Add sentry to capture exception
    return jsonify(e.to_dict()), error.to_status_code(e)
