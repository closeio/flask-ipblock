from setuptools import setup

setup(
    name='flask-ipblock',
    version='0.1',
    url='http://github.com/closeio/flask-ipblock',
    license='MIT',
    description='Block certain IP networks from accessing your Flask app',
    platforms='any',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
    ],
    packages=[
        'flask_ipblock',
    ],
)
