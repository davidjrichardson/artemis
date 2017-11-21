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
        r'(?P<karma_target>([^\"\s]+)|(\"([^\"]+)\"))(?P<karma_op>(\+\+|\+\-|\-\+|\-\-))(\s(because|for)\s+(?P<karma_reason>.+)$|\s\(.+\)+|\s|$)')
    result = karma_regex.search(filtered_message)

    # If there was no result then get return none - no need to go further
    if not result:
        return None

    return RawKarma(name=result.group('karma_target'), op=result.group('karma_op'), reason=result.group('karma_reason'))
