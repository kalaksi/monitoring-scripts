#!/bin/bash
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


# A script for standby-status metering for sensu (and graphite)
# Returns value of 1.0 for disks in standby or sleeping and 0.0 for others.

# ATTENTION! Using hdparm requires a limited root (sudo) access to hdparm!
# Example for a sudoers-file (for 3-letter device-names):
# Cmnd_Alias HDPARM_C = /sbin/hdparm -C /dev/[a-zA-Z][a-zA-Z][a-zA-Z]
# sensu ALL=NOPASSWD: HDPARM_C

if [ -z "$1" ]; then
    echo 'Disk device(s) needed as parameters (e.g. "sda")' >&2
    exit 1
fi

name=$(/bin/hostname)

for disk in "$@"; do

    # Process only if a valid block device
    if [ -b "/dev/$disk" ]; then
        status=$( (/usr/bin/sudo /sbin/hdparm -C "/dev/$disk" | /bin/grep -qi "drive\ state.*standby\|sleeping") \
                  && echo "1.0" || echo "0.0")

        echo "$name.disk_standby.$disk.in_standby $status $(/bin/date +%s)"

    # XXX: Optional error message
    # else
    #     echo "ERROR: not a block device: /dev/$disk" >&2

    fi
done
