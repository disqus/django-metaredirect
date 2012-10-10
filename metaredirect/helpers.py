import httpagentparser


def is_interactive_user_agent(request):
    """
    Returns if this request appears to have been made with an interactive user
    agent (e.g. a graphical browser).
    """
    properties = httpagentparser.detect(request.META.get('HTTP_USER_AGENT', ''))
    if not properties:
        return False

    try:
        browser = properties['browser']['name']
    except KeyError:
        return False

    return browser in ('Firefox', 'SeaMonkey', 'Konqueror', 'Opera', 'Netscape',
        'Microsoft Internet Explorer', 'Safari', 'Chrome')
