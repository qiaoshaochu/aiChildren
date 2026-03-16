from flask import jsonify


def unauthorized(message="未登录"):
  return jsonify({"error": message}), 401


def bad_request(message):
  return jsonify({"error": message}), 400


__all__ = ["unauthorized", "bad_request"]

