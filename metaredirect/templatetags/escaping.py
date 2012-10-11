from django import template


register = template.Library()


@register.filter
def escapeforwardslashes(value):
    """
    Escapes forward slashes in a string. For example, ``foo/bar`` becomes
    ``foo\/bar`` after the filter is applied.

    Useful for escaping slashes in URLs that will be used in an HTML <script>
    tag: http://stackoverflow.com/questions/1580647/

    This is possibly unnecessary when paired with the ``escapejs`` filter, but
    better safe then sorry.
    """
    return unicode(value).replace('/', '\/')
