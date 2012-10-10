import mock
from django.http import HttpRequest
from django.test import TestCase

from metaredirect.helpers import is_interactive_user_agent
from metaredirect.views import redirect_to


class InteractiveUserAgentTestCase(TestCase):
    INTERACTIVE_USER_AGENTS = (
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-GB; rv:1.9.0.10) Gecko/2009042315 Firefox/3.0.10',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_6) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.3 Safari/534.24,gzip(gfe)',
    )
    NONINTERACTIVE_USER_AGENTS = (
        'curl/7.21.4 (universal-apple-darwin11.0) libcurl/7.21.4 OpenSSL/0.9.8r zlib/1.2.5',
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


class RedirectToViewTestCase(TestCase):
    def get_response(self, url='http://example.com', *args, **kwargs):
        request = mock.Mock(spec=HttpRequest)
        return redirect_to(request, url, *args, **kwargs)

    @mock.patch('metaredirect.views.is_interactive_user_agent', return_value=True)
    def test_200_redirect_for_interactive_agent(self, *args):
        response = self.get_response()
        self.assertEqual(response.status_code, 200)

        meta_redirect = '<META http-equiv="refresh" content="0;URL=http://example.com">'
        self.assertContains(response, meta_redirect)

        javascript_redirect = '<script>location.replace("http:\/\/example.com")</script>'
        self.assertContains(response, javascript_redirect)

    @mock.patch('metaredirect.views.is_interactive_user_agent', return_value=False)
    def test_302_redirect_for_noninteractive_agent(self, *args):
        response = self.get_response()
        self.assertEqual(response.status_code, 302)

    @mock.patch('metaredirect.views.is_interactive_user_agent', return_value=False)
    def test_301_redirect_for_noninteractive_agent(self, *args):
        response = self.get_response(permanent=True)
        self.assertEqual(response.status_code, 301)

    @mock.patch('metaredirect.views.is_interactive_user_agent', return_value=True)
    def test_200_redirect_escaping(self, *args):
        response = self.get_response(url='http://example.com/")</script>')
        self.assertEqual(response.status_code, 200)

        meta_redirect = '<META http-equiv="refresh" content="0;URL=http://example.com/&quot;)&lt;/script&gt;">'
        self.assertContains(response, meta_redirect)

        javascript_redirect = r'<script>location.replace("http:\/\/example.com\/\u0022)\u003C\/script\u003E")</script>'
        self.assertContains(response, javascript_redirect)
