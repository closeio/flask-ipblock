from flask import request, url_for
from flask_ipblock.documents import IPNetwork


class IPBlock(object):
    def __init__(self, app, read_preference=None):
        """
        Initialize IPBlock and set up a before_request handler in the
        app.

        You can override the default MongoDB read preference via the
        optional read_preference kwarg.
        """
        self.read_preference = read_preference
        app.before_request(self.block_before)

    def block_before(self):
        """
        Check the current request and block it if the IP address it's
        coming from is blacklisted.
        """
        # To avoid unnecessary database queries, ignore the IP check for
        # requests for static files
        if request.path.startswith(url_for('static', filename='')):
            return

        # Some static files might be served from the root path (e.g.
        # favicon.ico, robots.txt, etc.). Ignore the IP check for most
        # common extensions of those files.
        ignored_extensions = ('ico', 'png', 'txt', 'xml')
        if request.path.rsplit('.', 1)[-1] in ignored_extensions:
            return

        ips = request.headers.getlist('X-Forwarded-For')
        if not ips:
            return

        # If the X-Forwarded-For header contains multiple comma-separated
        # IP addresses, we're only interested in the last one.
        ip = ips[0].strip()
        if ip[-1] == ',':
            ip = ip[:-1]
        ip = ip.rsplit(',', 1)[-1].strip()

        if IPNetwork.matches_ip(ip, read_preference=self.read_preference):
            return 'IP Blocked', 200
