#!/usr/bin/env python2
#
# Copyright (c) 2015 kalaksi@users.noreply.github.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import time
import re
from logster.logster_helper import MetricObject, LogsterParser
from logster.logster_helper import LogsterParsingException


class OssecAlertLogster(LogsterParser):
    """ A logster parser for OSSEC HIDS alert logs.
    Outputs count of alerts on different alert levels.
    """

    def __init__(self, option_string=None):

        # Count of alerts on levels 0-16
        self.levels = {}
        for i in range(17):
            self.levels[str(i)] = 0

        # Regular expression for matching different alert levels
        self.level_re = re.compile('^Rule:.*\(level (?P<level>.+)\) ->.*')


    def parse_line(self, line):
        try:
            # Apply regular expression to each line and extract interesting bits.
            match = self.level_re.match(line)

            if match:
                values = match.groupdict()
                alert_level = values['level']

                if (alert_level in self.levels):
                    self.levels[alert_level] += 1
                else:
                    raise LogsterParsingException, "Unknown alert level '%s'" % alert_level

        except Exception, e:
            raise LogsterParsingException, "Error while parsing a line: %s" % e


    def get_state(self, duration):

        # Compile a list of alert counts
        result = []
        for level, count in self.levels.iteritems():
            result.append(MetricObject("level_"+level, count, "Error count of level "+level))

        return result
