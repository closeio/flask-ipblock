Flask-IPBlock [![Build Status](https://circleci.com/gh/closeio/flask-ipblock.png?branch=master&style=shield)](https://circleci.com/gh/closeio/flask-ipblock)
=============

Block certain IP addresses from accessing your Flask application.

Flask-IPBlock is backed by MongoDB and supports application-level caching to boost performance.

Setup
=====

``` python
from flask import Flask
from flask_ipblock import IPBlock
from flask_ipblock.documents import IPNetwork

# Initialize the Flask app
app = Flask(__name__)

# Configuration (e.g. setting up MongoEngine)
# (...)

# Set up IPBlock
ipblock = IPBlock(app)

# Create a MongoEngine document corresponding to a range of IP addresses
# owned by Facebook
IPNetwork.objects.create_from_string('204.15.20.0/22', label='Facebook')

# From now on, any request coming from the above range will be blocked.
```
