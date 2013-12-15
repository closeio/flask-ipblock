from flask import request
from flask.ext.ipblock.documents import IPNetwork

class IPBlock(object):
    def __init__(self, app):
        app.before_request(self.block_before)

    def block_before(self):
        ips = request.headers.getlist("X-Forwarded-For")
        if ips and IPNetwork.matches_ip(ips[0]):
            return '', 200
