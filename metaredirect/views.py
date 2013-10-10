from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.utils.encoding import iri_to_uri

from metaredirect.helpers import is_interactive_user_agent


def templated_redirect_response(url):
    response = render_to_response('metaredirect/redirect.txt', {
        'url': url,
    })
    try:
        response['X-Location'] = url.encode('ascii')
    except UnicodeEncodeError:
        response['X-Location'] = iri_to_uri(url)
    return response


def redirect_to(request, url, permanent=False):
    """
    A generic view for redirecting to the provided URL, using a HTTP 200
    response with a META-tag based redirect for whitelisted interactive
    browsers, and falling back to a 300-class HTTP standard redirect for
    non-interactive browers.

    :param request: the original HTTP request triggering the response
    :type request: :class:`django.http.HttpRequest`
    :param url: the URL to redirect to
    :type url: :class:`str`
    :param permanent: if the redirect is permanent or not. Only used for
        non-interactive clients.
    :type permanent: :class:`bool`
    :returns: an HTTP response
    :rtype: :class:`django.http.HttpResponse` or derived class
    """
    if is_interactive_user_agent(request):
        return templated_redirect_response(url)
    else:
        if permanent:
            response_cls = HttpResponsePermanentRedirect
        else:
            response_cls = HttpResponseRedirect
        return response_cls(url)
