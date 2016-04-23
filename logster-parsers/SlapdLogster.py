#!/usr/bin/env python2                                                                                                                                                                
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 kalaksi@users.noreply.github.com
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

class SlapdLogster(LogsterParser):
    """ A logster parser for slapd, the openldap daemon
    """

    def __init__(self, option_string=None):
        # Modify monitored_tags according to your needs. 
        # The key is the tag code and the value is a dict that has:
        # - name: arbitrary name for the metric
        # - success: match count for successes (err=0)
        # - error: match count for other error codes
        # In other words, the script doesn't differentiate between error codes, 
        # which should be enough for most use-cases.
        # 
        # Reference for tag codes (I wish I had a shorter URL...):
        # https://access.redhat.com/documentation/en-US/Red_Hat_Directory_Server/8.0/html/Configuration_and_Command_Reference/Configuration_Command_File_Reference-Access_Log_and_Connection_Code_Reference.html

        self.monitored_tags = { 
            97: {'name': 'bind', 'success': 0, 'error': 0} 
        }

        # The regular expression for every line
        self.line_re = re.compile('.* RESULT tag=(?P<tag>\w+) err=(?P<error>\w+) .*')

    def parse_line(self, line):
        try:
            match = self.line_re.match(line)

            # Only care about the lines that match
            if match:
                values = match.groupdict()
                tag = int(values['tag'])
                error_code = int(values['error'])

                if tag in self.monitored_tags:
                    if error_code == 0:
                        self.monitored_tags[tag]['success'] += 1
                    else:
                        self.monitored_tags[tag]['error'] += 1

        except Exception, e:
            raise LogsterParsingException, "Error while parsing a line: %s" % e


    def get_state(self, duration):
        result = []

        for tag, data in self.monitored_tags.iteritems():
            result.append(MetricObject(data['name']+'_success', data['success'], 'Tag '+data['name']+': successes'))
            result.append(MetricObject(data['name']+'_error', data['error'], 'Tag '+data['name']+': errors'))

        return result

