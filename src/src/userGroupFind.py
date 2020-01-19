# -*- coding: utf-8 -*-
#
# userGroupFind.py - find new user and group ids according to prefs
# Copyright © 2006, 2007, 2009 - 2011 Red Hat, Inc.
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

import libuser

from constants import (uid_min, gid_min, high_uid_ignore, high_gid_ignore,
        mininvalidid)


class DuplicateUidNumberError(Exception):
    def __init__(self, uidNumber):
        self.uidNumber = uidNumber


class DuplicateGidNumberError(Exception):
    def __init__(self, gidNumber):
        self.gidNumber = gidNumber


class IdSpaceExceededError(Exception):
    def __init__(self, uidNumber=None, gidNumber=None):
        self.uidNumber = uidNumber
        self.gidNumber = gidNumber


def find_uid_gid(lu_admin, preferences, uidNumber=None, gidNumber=None):
    """Try to find a free uid/gid number pair based on preferences, eventually
    with a given uid number."""

    # get all users
    users = lu_admin.enumerateUsersFull()
    # hide some
    usersNotHidden = filter(lambda x: x[libuser.USERNAME][0] not in
            high_uid_ignore, users)
    # get their UIDs
    uidNumbers = []
    for u in usersNotHidden:
        try:
            uidNumbers.append(u[libuser.UIDNUMBER][0])
        except KeyError:
            # e.g. entry only in /etc/shadow
            pass

    if uidNumber == None:
        uidNumber = uid_min
        if preferences['ASSIGN_HIGHEST_UID']:
            for uidNum in uidNumbers:
                if uidNum > uidNumber:
                    uidNumber = uidNum + 1
        while uidNumber in uidNumbers:
            uidNumber += 1
        while gidNumber == None or uidNumber in uidNumbers:
            if uidNumber not in uidNumbers:
                try:
                    gidNumber = find_gid(lu_admin, preferences,
                            preferences['PREFER_SAME_UID_GID'] and
                            uidNumber or None)
                except DuplicateGidNumberError:
                    uidNumber += 1
            else:
                uidNumber += 1
    else:
        if uidNumber in uidNumbers:
            raise DuplicateUidNumberError(uidNumber)
    try:
        if gidNumber is None:
            if preferences['PREFER_SAME_UID_GID']:
                _gid = uidNumber
            else:
                _gid = None
        else:
            _gid = gidNumber
        gidNumber = find_gid(lu_admin, preferences, _gid)
    except IdSpaceExceededError:
        # handled below
        pass

    if uidNumber >= mininvalidid or gidNumber >= mininvalidid:
        raise IdSpaceExceededError(uidNumber=uidNumber, gidNumber=gidNumber)

    return uidNumber, gidNumber


def find_gid(lu_admin, preferences, gidNumber=None):
    """Try to find a free gid number based on preferences, eventually with a
    given gid number."""

    # get all groups
    groups = lu_admin.enumerateGroupsFull()
    # hide some
    groupsNotHidden = filter(lambda x: x[libuser.GROUPNAME][0] not in
            high_gid_ignore, groups)
    # get their GIDs
    gidNumbers = []
    for g in groupsNotHidden:
        try:
            gidNumbers.append(g[libuser.GIDNUMBER][0])
        except KeyError:
            # e.g. entry only in /etc/gshadow
            pass

    if gidNumber == None:
        gidNumber = gid_min
        if preferences['ASSIGN_HIGHEST_GID']:
            for gidNum in gidNumbers:
                if gidNum > gidNumber:
                    gidNumber = gidNum + 1
        while gidNumber in gidNumbers:
            gidNumber += 1
    else:
        if gidNumber in gidNumbers:
            raise DuplicateGidNumberError(gidNumber)

    if gidNumber >= mininvalidid:
        raise IdSpaceExceededError(gidNumber=gidNumber)

    return gidNumber
