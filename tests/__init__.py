import unittest

from flask_ipblock.documents import IPNetwork

from mongoengine.connection import connect

connect('testdb')


class IPBlockTestCase(unittest.TestCase):

    def setUp(self):
        IPNetwork.drop_collection()

    def test_blacklist_specific_ip(self):
        IPNetwork.create_from_string('192.168.1.23/32')
        self.assertTrue(IPNetwork.matches_ip('192.168.1.23'))
        self.assertFalse(IPNetwork.matches_ip('192.168.1.22'))
        self.assertFalse(IPNetwork.matches_ip('192.168.1.24'))
        self.assertFalse(IPNetwork.matches_ip('192.168.100.23'))

    def test_blacklist_ip_range(self):
        IPNetwork.create_from_string('192.168.1.0/24')
        for i in range(256):
            self.assertTrue(IPNetwork.matches_ip('192.168.1.%d' % i))
        self.assertFalse(IPNetwork.matches_ip('192.168.2.1'))

    def test_whitelist_ip(self):
        # blacklist the whole range
        IPNetwork.create_from_string('192.168.1.0/24')

        # whitelist a single address
        IPNetwork.create_from_string('192.168.1.100/32', whitelist=True)

        for i in range(256):
            match = IPNetwork.matches_ip('192.168.1.%d' % i)
            if i == 100:
                self.assertFalse(match)
            else:
                self.assertTrue(match)

    def test_ipv6(self):
        """Make sure an IPv6 address is ignored gracefully for now."""
        self.assertFalse(IPNetwork.matches_ip('2604:a880:800:10::ff:1'))


if __name__ == '__main__':
    unittest.main()
