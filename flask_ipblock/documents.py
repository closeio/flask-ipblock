import netaddr
from mongoengine import *

class IPNetwork(Document):
    """
    Represents an IP (v4 or v6) network as 2 integers, the starting address and the stopping address, inclusive.
    """
    label = StringField(required=False)
    start = IntField(required=True)
    stop = IntField(required=True)

    meta = {
        'indexes': [('start', 'stop')]
    }

    @classmethod
    def create_from_string(cls, cidr, label=None):
        """
        Converts a CIDR like 192.168.0.0/24 into 2 parts:
            start: 3232235520
            stop: 3232235775
        """
        network = netaddr.IPNetwork(cidr)
        start = network.first
        stop = start + network.size - 1
        obj = cls.objects.create(label=label, start=start, stop=stop)
        return obj

    def __unicode__(self):
        return "%s: %s - %s" % (self.label, str(netaddr.IPAddress(self.start)), str(netaddr.IPAddress(self.stop)))

    @classmethod
    def matches_ip(cls, ip_str):
        ip = int(netaddr.IPAddress(ip_str))
        return (cls.objects.filter(start__lte=ip, stop__gte=ip).count() > 0)
