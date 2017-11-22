import re

from collections import namedtuple

RawKarma = namedtuple('RawKarma', ['name', 'op', 'reason'])


def parse_message(message: str):
    # Remove any code blocks
    filtered_message = re.sub(u'```.*```', '', message)

    # If there's no message to parse then there's nothing to return
    if not filtered_message:
        return None

    # The regex for parsing karma messages
    # Hold on tight because this will be a doozy...
    karma_regex = re.compile(
        r'(?P<karma_target>([^\"\s]+)|(\"([^\"]+)\"))(?P<karma_op>(\+\+|\+\-|\-\+|\-\-))(\s(because|for)\s+(?P<karma_reason>[^,]+)($|,)|\s\(.+\)+|,?\s|$)')
    items = karma_regex.finditer(filtered_message)
    results = []

    # Collate all matches into a list
    for item in items:
        results.append(RawKarma(name=item.group('karma_target'), op=item.group('karma_op'), reason=item.group('karma_reason')))

    # If there are any results then return the list, otherwise give None
    if results:
        return results
    else:
        return None
