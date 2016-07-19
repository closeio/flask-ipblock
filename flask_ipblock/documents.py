import netaddr
from mongoengine import Document, StringField, IntField, BooleanField


class IPNetwork(Document):
    """
    Represents an IP (v4 or v6) network as 2 integers, the starting address
    and the stopping address, inclusive.
    """
    label = StringField(required=False)
    start = IntField(required=True)
    stop = IntField(required=True)
    whitelist = BooleanField(default=False)

    meta = {
        'indexes': [('start', 'stop', 'whitelist')]
    }

    @classmethod
    def create_from_string(cls, cidr, label=None, whitelist=False):
        """
        Converts a CIDR like 192.168.0.0/24 into 2 parts:
            start: 3232235520
            stop: 3232235775
        """
        network = netaddr.IPNetwork(cidr)
        start = network.first
        stop = start + network.size - 1
        obj = cls.objects.create(label=label, start=start, stop=stop,
                                 whitelist=whitelist)
        return obj

    def __unicode__(self):
        return "%s: %s - %s" % (
            self.label,
            str(netaddr.IPAddress(self.start)),
            str(netaddr.IPAddress(self.stop)))

    @classmethod
    def qs_for_ip(cls, ip_str):
        """
        Returns a queryset with matching IPNetwork objects for the given IP.
        """
        ip = int(netaddr.IPAddress(ip_str))

        # ignore IPv6 addresses for now (4294967295 is 0xffffffff, aka the
        # biggest 32-bit number)
        if ip > 4294967295:
            return cls.objects.none()

        ip_range_query = {
            'start__lte': ip,
            'stop__gte': ip
        }

        return cls.objects.filter(**ip_range_query)

    @classmethod
    def matches_ip(cls, ip_str, read_preference=None):
        """
        Return True if provided IP exists in the blacklist and doesn't exist
        in the whitelist. Otherwise, return False.
        """
        qs = cls.qs_for_ip(ip_str).only('whitelist')
        if read_preference:
            qs = qs.read_preference(read_preference)

        # Return True if any docs match the IP and none of them represent
        # a whitelist
        return bool(qs) and not any(obj.whitelist for obj in qs)
