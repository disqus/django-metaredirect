from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from metaredirect.helpers import is_interactive_user_agent


def redirect_to(request, url, permanent=False):
    if is_interactive_user_agent(request):
        context = RequestContext(request, {'url': url})
        return render_to_response('metaredirect/redirect.txt',
            context_instance=context)
    else:
        if permanent:
            response_cls = HttpResponsePermanentRedirect
        else:
            response_cls = HttpResponseRedirect
        return response_cls(url)
