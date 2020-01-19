# -*- coding: utf-8 -*-
#
# fbutil.py - tweak some things when running in firstboot
# Copyright © 2012 Red Hat, Inc.
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


import gtk
import time

running_in_firstboot = False
_tweaked_toplevels = set()


def _on_window_state_event(toplevel, event):
    if (event.changed_mask & gtk.gdk.WINDOW_STATE_ICONIFIED and
            event.new_window_state & gtk.gdk.WINDOW_STATE_ICONIFIED):
        toplevel.deiconify()
        now = time.localtime()
        if now.tm_mday == 1 and now.tm_mon == 4:
            # Sorry, Dude
            dlg = gtk.Dialog(title="Walter says:", parent=toplevel,
                    flags=gtk.DIALOG_MODAL,
                    buttons=("Huh?", gtk.RESPONSE_ACCEPT))
            dlg.set_border_width(5)
            vbox = dlg.get_content_area()
            vbox.set_spacing(5)
            l = gtk.Label("OVER THE LINE!")
            vbox.pack_end(l)
            dlg.show_all()
            dlg.run()
            dlg.destroy()
    return False


def handle_firstboot(toplevel):
    # only in firstboot... and guard against repeated calls for the same
    # toplevel
    if not running_in_firstboot or toplevel in _tweaked_toplevels:
        return

    _tweaked_toplevels.add(toplevel)

    # toplevels shouldn't be minimized when running in firstboot
    toplevel.connect("window-state-event", _on_window_state_event)
