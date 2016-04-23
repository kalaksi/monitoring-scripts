#!/usr/bin/env python2                                                                                                                                                                
# -*- coding: utf-8 -*-
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

class ShorewallLogster(LogsterParser):
    """ A logster parser for Shorewall logs.
    Intended for separate ulog/nflog file, not syslog. 
    """

    def __init__(self, option_string=None):
        # To track count of a new action or protocol you only have 
        # to initialize it here
        self.actions = { 'drop': 0, 'reject': 0 }
        self.protocols = { 'tcp': 0, 'udp': 0, 'icmp': 0 }

        # The regular expression for every line
        self.line_re = re.compile('.*Shorewall:[\w-]+:(?P<action>\w+):.* PROTO=(?P<protocol>\w+) .*')

    def parse_line(self, line):
        try:
            match = self.line_re.match(line)

            if match:
                values = match.groupdict()
                action = values['action'].lower()
                protocol = values['protocol'].lower()

                if action in self.actions:
                    self.actions[action] += 1

                if protocol in self.protocols:
                    self.protocols[protocol] += 1

            else:
                raise LogsterParsingException, "Match failed. Log line format is unknown."

        except Exception, e:
            raise LogsterParsingException, "Error while parsing a line: %s" % e


    def get_state(self, duration):
        result = []

        for action, count in self.actions.iteritems():
            result.append(MetricObject("action_"+action, count, "Action: "+action.upper()))

        for protocol, count in self.protocols.iteritems():
            result.append(MetricObject("proto_"+protocol, count, "Protocol: "+protocol.upper()))

        return result

