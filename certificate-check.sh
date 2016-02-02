#!/bin/bash
# The MIT License (MIT)
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


# Checks certificate expiration date of files matching CERT_FILES pattern and
# emails a specified recipient.
# If WARN_RECIPIENT is empty, certificate name and expiration date is printed to stdout.

CERT_FILES="/etc/ssl/*.crt"
WARN_DAYS_BEFORE=20
WARN_RECIPIENT=""


for cert_file in $CERT_FILES; do
    days_in_seconds=$(($WARN_DAYS_BEFORE * 24 * 60 * 60))

    if ! /usr/bin/openssl x509 -in "$cert_file" -checkend $days_in_seconds &>/dev/null; then
        cf_basename=$(basename "$cert_file")
        expiration_date=$(/usr/bin/openssl x509 -in "$cert_file" -enddate -noout | /bin/sed 's/.*=//g')

        if [ -z "$WARN_RECIPIENT" ]; then
            echo "$cf_basename: $expiration_date"
        else
            message="Subject: Certificate expiration warning\n\nCertificate $cf_basename is about to expire!\nExpiration date: $expiration_date."
            echo -e $message | /usr/sbin/sendmail -t "$WARN_RECIPIENT"
        fi
    fi
done
