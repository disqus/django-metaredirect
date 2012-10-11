django-metaredirect
===================

A simple pluggable Django application that allows maintaining internal HTTP
referrers for external links by using META-tag or JavaScript based redirects for
interactive user agents (e.g. graphical browers), while falling back to standard
HTTP response classes (301 and 302 status codes) for non-interactive clients.

Installation
------------

#. Add ``metaredirect`` to your project's ``INSTALLED_APPS`` settings.
#. Instead of using ``django.views.generic.simple.redirect_to`` or plain
   ``HttpResponseRedirect``/``HttpResponsePermanentRedirect`` response classes for
   view responses, use ``metaredirect.views.redirect_to``.

Testing
-------

``make test`` and ``make test-matrix``

Testing in Your Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To ensure a HTTP 200 redirect is the response for a given request, check the
presence and value of the ``X-Location`` header in the response for a browser
user-agent.
