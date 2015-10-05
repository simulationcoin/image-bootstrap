# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under AGPL v3 or later

from __future__ import print_function

import re

_year = '([2-9][0-9]{3})'
_month = '(0[1-9]|1[12])'
_day = '(0[1-9]|[12][0-9]|3[01])'

_STAGE3_TARBALL_DATE_PATTERN = '^(?P<date>%s%s%s)/stage3-(?P<arch>[^ -]+)-[0-9]+\\.tar\\.[^ ]+ [1-9]+[0-9]*$' % (_year, _month, _day)
_stage3_tarball_date_matcher = re.compile(_STAGE3_TARBALL_DATE_PATTERN)


def find_latest_stage3_date(stage3_latest_file_content, stage3_latest_file_url, architecture):
    matches = []
    for line in stage3_latest_file_content.split('\n'):
        m = _stage3_tarball_date_matcher.match(line)
        if m is None:
            continue
        if m.group('arch') != architecture:
            continue
        matches.append(m)

    message = ('Content from %s does not seem to contain '
            'a single (or mutliple agreeing) well-formed default flavour '
            'stage3 tarball entr(y|ies)'
            % stage3_latest_file_url
            )

    if not matches:
        raise ValueError(message)

    date_strs = list(set([m.group(1) for m in matches]))
    if len(date_strs) != 1:
        raise ValueError(message)

    m = matches[0]
    return int(m.group(2)), int(m.group(3)), int(m.group(4))
