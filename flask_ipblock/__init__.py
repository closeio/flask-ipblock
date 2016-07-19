from flask import request, url_for
from flask.ext.ipblock.documents import IPNetwork


class IPBlock(object):
    def __init__(self, app, use_secondary=False):
        """
        Initialize IPBlock and set up a before_request handler in the app.

        If use_secondary is True, MongoDB query in IPNetwork.matches_ip will
        use a secondaryPreferred option.
        """
        self.use_secondary = use_secondary
        app.before_request(self.block_before)

    def block_before(self):

        # To avoid unnecessary database queries, ignore the IP check for
        # requests for static files
        if request.path.startswith(url_for('static', filename='')):
            return
        # Some static files are served from the root path
        ignored_extensions = ('ico', 'png', 'txt', 'xml')
        if request.path.rsplit('.', 1)[-1] in ignored_extensions:
            return

        ips = request.headers.getlist("X-Forwarded-For")
        if not ips:
            return

        ip = ips[0].strip()
        if ip[-1] == ',':
            ip = ip[:-1]
        ip = ip.rsplit(',', 1)[-1].strip()

        if IPNetwork.matches_ip(ip, use_secondary=self.use_secondary):
            return 'IP Blocked', 200
