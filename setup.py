#!/usr/bin/env python
import os
import sys

from setuptools import find_packages, setup


def get_version():
    from metaredirect import __version__
    return '.'.join(map(str, __version__))

try:
    version = get_version()
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'metaredirect'))
    version = get_version()


install_requires = ['django', 'httpagentparser']
tests_require = ['mock']

setup(name='django-metaredirect',
    version=version,
    url='http://github.com/disqus/django-metaredirect/',
    author='Disqus',
    author_email='opensource@disqus.com',
    description='META-tag and JavaScript based generic redirect views for '
        'maintaining HTTP referrers.',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    license='Apache License 2.0',
    tests_require=tests_require,
    test_suite='metaredirect.tests.run',
    zip_safe=False,
)
