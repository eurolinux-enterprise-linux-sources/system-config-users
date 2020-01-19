# -*- coding: utf-8 -*-
#
# constants.py - system and other constants
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
# Nils Philippsen <nils@redhat.com>

import os
import libuser

from util import parse_login_defs

# maximum length of user and group names
maxusernamelength = maxgroupnamelength = libuser.UT_NAMESIZE - 1

# maximum length of file names and paths
maxfilenamelength = os.pathconf('/', os.pathconf_names['PC_NAME_MAX'])
maxpathlength = os.pathconf('/', os.pathconf_names['PC_PATH_MAX'])

# minimum and maximum ids for (normal) users and groups
__logindefs = parse_login_defs()

__uid_min_default = __gid_min_default = 1000
__uid_max_default = __gid_max_default = 60000

__globals = globals()
for __var in ('uid_min', 'gid_min', 'uid_max', 'gid_max'):
    try:
        __globals[__var] = int(__logindefs[__var.upper()])
    except (KeyError, ValueError):
        __globals[__var] = __globals['__' + __var + '_default']

try:
    mininvalidid = libuser.VALUE_INVALID_ID
except AttributeError:
    # young Zaphod plays it safe
    mininvalidid = (1 << 16) - 1

# high uids/gids to ignore when determining uids/gids automatically or listing
# users and groups
__high_uid_gid_ignore = ('nfsnobody',)
high_uid_ignore = __high_uid_gid_ignore
high_gid_ignore = __high_uid_gid_ignore

__high_uid_gid_ignore_numerical = (65534L, 4294967294L)
high_uid_ignore_numerical = __high_uid_gid_ignore_numerical
high_gid_ignore_numerical = __high_uid_gid_ignore_numerical
