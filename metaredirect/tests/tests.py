# -*- coding: utf-8 -*-
import mock
from django.http import HttpRequest
from django.template import Context, Template
from django.test import TestCase

from metaredirect.helpers import is_interactive_user_agent
from metaredirect.views import redirect_to


class InteractiveUserAgentTestCase(TestCase):
    INTERACTIVE_USER_AGENTS = (
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-GB; rv:1.9.0.10) '
            'Gecko/2009042315 Firefox/3.0.10',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_6) AppleWebKit/534.24 '
            '(KHTML, like Gecko) Chrome/11.0.696.3 Safari/534.24,gzip(gfe)',
    )
    NONINTERACTIVE_USER_AGENTS = (
        'curl/7.21.4 (universal-apple-darwin11.0) libcurl/7.21.4 '
            'OpenSSL/0.9.8r zlib/1.2.5',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) '
            'AppleWebKit/534.46 (KHTML, like Gecko) Mobil',  # parses incorrectly
    )

    def get_request_for_user_agent(self, agent):
        request = mock.Mock(spec=HttpRequest)
        request.META = {}
        if agent is not None:
            request.META['HTTP_USER_AGENT'] = agent
        return request

    def test_interactive_user_agents(self):
        for agent in self.INTERACTIVE_USER_AGENTS:
            request = self.get_request_for_user_agent(agent)
            self.assertTrue(is_interactive_user_agent(request))

    def test_noninteractive_user_agents(self):
        for agent in self.NONINTERACTIVE_USER_AGENTS:
            request = self.get_request_for_user_agent(agent)
            self.assertFalse(is_interactive_user_agent(request))

    def test_no_user_agent(self):
        request = self.get_request_for_user_agent(None)
        self.assertFalse(is_interactive_user_agent(request))


def using_interactive_user_agent(value):
    stub = mock.Mock(return_value=value)
    return mock.patch('metaredirect.views.is_interactive_user_agent', stub)


class RedirectToViewTestCase(TestCase):

    def get_response(self, url='http://example.com', *args, **kwargs):
        request = mock.Mock(spec=HttpRequest)
        return redirect_to(request, url, *args, **kwargs)

    @using_interactive_user_agent(True)
    def test_200_redirect_for_interactive_agent(self):
        url = 'http://example.com'
        response = self.get_response(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Location'], url)

        meta_redirect = \
            '<META http-equiv="refresh" content="0;URL=http://example.com">'
        self.assertContains(response, meta_redirect)

        javascript_redirect = \
            '<script>window.opener=null;location.replace("http:\/\/example.com")</script>'
        self.assertContains(response, javascript_redirect)

    @using_interactive_user_agent(False)
    def test_302_redirect_for_noninteractive_agent(self):
        response = self.get_response()
        self.assertEqual(response.status_code, 302)

    @using_interactive_user_agent(False)
    def test_301_redirect_for_noninteractive_agent(self):
        response = self.get_response(permanent=True)
        self.assertEqual(response.status_code, 301)

    @using_interactive_user_agent(True)
    def test_200_redirect_escaping(self):
        response = self.get_response(url='http://example.com/")</script>')
        self.assertEqual(response.status_code, 200)

        meta_redirect = '<META http-equiv="refresh" ' \
            'content="0;URL=http://example.com/&quot;)&lt;/script&gt;">'
        self.assertContains(response, meta_redirect)

        javascript_redirect = r'<script>window.opener=null;location.replace' \
            '("http:\/\/example.com\/\u0022)\u003C\/script\u003E")</script>'
        self.assertContains(response, javascript_redirect)

    @using_interactive_user_agent(True)
    def test_encodes_utf8_url(self):
        location = u'http://disqus.com/☃'
        try:
            response = self.get_response(location)
        except UnicodeEncodeError:
            self.fail('Should encode UTF-8 locations')

        self.assertEqual(response['X-Location'], 'http://disqus.com/%E2%98%83')


class EscapeForwardSlashesTestCase(TestCase):
    template = Template('{% load escaping %}{{ value|escapeforwardslashes }}')

    def test_escapes_slashes(self):
        self.assertEqual(self.template.render(Context({
            'value': 'foo/bar',
        })), 'foo\/bar')
