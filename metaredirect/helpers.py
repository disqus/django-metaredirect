import httpagentparser
import logging


logger = logging.getLogger(__name__)


def is_interactive_user_agent(request):
    """
    Returns if this request appears to have been made with an interactive user
    agent (e.g. a graphical browser).
    """
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    properties = httpagentparser.detect(user_agent)
    if not properties:
        return False

    browser = properties.get('browser')

    # XXX: `httpagentparser.Result` overrides `dict.__missing__` to return an
    # empty string instead of raising a `KeyError`. In this case, we can't make
    # a reasonable judgement about what browser this is, so just assume it's
    # not an interactive one.
    if not browser:
        logger.info('Skipping unparsable user agent: %s', user_agent)
        return False

    return browser['name'] in ('Firefox', 'SeaMonkey', 'Konqueror', 'Opera',
        'Netscape', 'Microsoft Internet Explorer', 'Safari', 'Chrome')
