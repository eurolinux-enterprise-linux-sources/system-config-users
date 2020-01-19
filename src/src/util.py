# -*- coding: utf-8 -*-
#
# util.py - miscellaneous utility functions
# Copyright © 2011 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# Authors:
# Miloslav Trmač <mitr@redhat.com>

import re

__all__ = ["parse_login_defs"]

# No, this is not particularly nice, but "compatible" is more important than
# "beautiful".
__ld_line = re.compile(r'^[ \t]*'         # Initial whitespace
                       r'([^ \t]+)'       # Variable name
                       r'[ \t][ \t"]*'    # Separator - yes, may have multiple
                                          # '"'s
                       r'(([^"]*)".*'     # Value, case 1 - terminated by '"'
                       r'|([^"]*\S)?\s*'  # Value, case 2 - only drop trailing
                                          # '\'s
                       r')$')


def parse_login_defs():
    res = {}
    with open('/etc/login.defs') as f:
        for line in f:
            match = __ld_line.match(line)
            if match is not None:
                name = match.group(1)
                if name.startswith('#'):
                    continue
                value = match.group(3)
                if value is None:
                    value = match.group(4)
                    if value is None:
                        value = ''
                res[name] = value  # Override previous definition
    return res
