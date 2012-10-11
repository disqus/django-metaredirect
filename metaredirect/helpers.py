import httpagentparser


def is_interactive_user_agent(request):
    """
    Returns if this request appears to have been made with an interactive user
    agent (e.g. a graphical browser).
    """
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    properties = httpagentparser.detect(user_agent)
    if not properties:
        return False

    try:
        browser = properties['browser']['name']
    except KeyError:
        return False

    return browser in ('Firefox', 'SeaMonkey', 'Konqueror', 'Opera',
        'Netscape', 'Microsoft Internet Explorer', 'Safari', 'Chrome')
