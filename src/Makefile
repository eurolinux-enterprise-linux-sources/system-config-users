# License: GPL v2 or later
# Copyright Red Hat Inc. 2001 - 2008

PKGNAME=system-config-users

SCM_REMOTEREPO_RE = ^ssh://(.*@)?git.fedorahosted.org/git/$(PKGNAME).git$
UPLOAD_URL = ssh://fedorahosted.org/$(PKGNAME)

PREFIX=/usr

BINDIR=${PREFIX}/bin
DATADIR=${PREFIX}/share
MANDIR=${DATADIR}/man

PKGDATADIR=${DATADIR}/${PKGNAME}

SYSCONFDIR		= /etc
SYSCONFIG_DIR	= ${SYSCONFDIR}/sysconfig

POLKIT_FILES=config/org.fedoraproject.config.users.policy
PKEXEC_SCRIPT_IN=src/system-config-users.sh.in
PKEXEC_SCRIPT=$(BINDIR)/system-config-users
PKEXEC_SCRIPT_DEST=$(PKGDATADIR)/system-config-users.py

PY_SOURCES		= $(wildcard src/*.py)

GLADE_SOURCES	= $(wildcard src/*.glade)

PO_SOURCES		= $(PY_SOURCES) $(PO_GLADEH_FILES) $(DESKTOPINH_FILES)

all:	po-all desktop-all polkit-all

include rpmspec_rules.mk
include git_rules.mk
include upload_rules.mk
include desktop_rules.mk
include polkit_rules.mk
include po_rules.mk

install:	all po-install desktop-install polkit-install
	mkdir -p $(DESTDIR)$(PKGDATADIR)
	mkdir -p $(DESTDIR)$(PKGDATADIR)/pixmaps
	mkdir -p $(DESTDIR)$(DATADIR)/icons/hicolor/48x48/apps
	mkdir -p $(DESTDIR)$(SYSCONFIG_DIR)
	mkdir -p $(DESTDIR)$(MANDIR)/man8
	for py in src/*.py ; do \
		sed -e s,@VERSION@,$(VERSION),g $${py} > $(DESTDIR)$(PKGDATADIR)/`basename $${py}` ; \
		chmod 0644 $(DESTDIR)$(PKGDATADIR)/`basename $${py}` ; \
	done
	chmod 0755 $(DESTDIR)$(PKGDATADIR)/system-config-users.py
	install -m 0644 src/${PKGNAME}.glade $(DESTDIR)$(PKGDATADIR)
	install -m 0644 ${PKGNAME}.prefs $(DESTDIR)$(SYSCONFIG_DIR)/${PKGNAME}
	install -m 0644 pixmaps/*.png $(DESTDIR)$(PKGDATADIR)
	install -m 0644 man/system-config-users.8 $(DESTDIR)$(MANDIR)/man8/
	python -c 'import compileall; compileall.compile_dir ("'"$(DESTDIR)$(PKGDATADIR)"'", ddir="'"$(PKGDATADIR)"'", maxlevels=10, force=1)'

clean: po-clean desktop-clean polkit-clean
	@rm -fv *~
	@rm -fv *.pyc
