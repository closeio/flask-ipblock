from flask import request
from flask.ext.ipblock.documents import IPNetwork

class IPBlock(object):
    def __init__(self, app):
        app.before_request(self.block_before)

    def block_before(self):
        ips = request.headers.getlist("X-Forwarded-For")
        if ips:
            ip = ips[0].strip()
            if ip[-1] == ',':
                ip = ip[:-1]
            if IPNetwork.matches_ip(ip.rsplit(',', 1)[-1].strip()):
                return '', 200
