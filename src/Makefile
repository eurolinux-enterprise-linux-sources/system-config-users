# License: GPL v2 or later
# Copyright Red Hat Inc. 2001 - 2008

PKGNAME=system-config-users

SCM_REMOTEREPO_RE = ^ssh://(.*@)?git.fedorahosted.org/git/$(PKGNAME).git$
UPLOAD_URL = ssh://fedorahosted.org/$(PKGNAME)

SUBDIRS=po

PREFIX=/usr

BINDIR=${PREFIX}/bin
DATADIR=${PREFIX}/share
MANDIR=${DATADIR}/man

PKGDATADIR=${DATADIR}/${PKGNAME}

SYSCONFDIR		= /etc
PAMD_DIR        = ${SYSCONFDIR}/pam.d
SECURITY_DIR    = ${SYSCONFDIR}/security/console.apps
SYSCONFIG_DIR	= ${SYSCONFDIR}/sysconfig

all:	$(PKGNAME).desktop $(PKGNAME).console

include rpmspec_rules.mk
include console_rules.mk
include git_rules.mk
include upload_rules.mk

po/$(PKGNAME).pot:: subdirs

subdirs:	$(PKGNAME).desktop.in.h
	for d in $(SUBDIRS); do make -C $$d; [ $$? = 0 ] || exit 1; done

%.desktop.in.h:	%.desktop.in
	intltool-extract --type=gettext/ini $<

%.desktop: %.desktop.in po/$(PKGNAME).pot po/*.po
	intltool-merge -u -d po/ $< $@

install:	all
	mkdir -p $(DESTDIR)$(BINDIR)
	mkdir -p $(DESTDIR)$(PKGDATADIR)
	mkdir -p $(DESTDIR)$(PKGDATADIR)/pixmaps
	mkdir -p $(DESTDIR)$(PAMD_DIR)
	mkdir -p $(DESTDIR)$(SECURITY_DIR)
	mkdir -p $(DESTDIR)$(DATADIR)/applications
	mkdir -p $(DESTDIR)$(DATADIR)/icons/hicolor/48x48/apps
	mkdir -p $(DESTDIR)$(SYSCONFIG_DIR)
	mkdir -p $(DESTDIR)$(MANDIR)/man8
	for py in src/*.py ; do \
		sed -e s,@VERSION@,$(VERSION),g $${py} > $(DESTDIR)$(PKGDATADIR)/`basename $${py}` ; \
		chmod 0644 $(DESTDIR)$(PKGDATADIR)/`basename $${py}` ; \
	done
	chmod 0755 $(DESTDIR)$(PKGDATADIR)/system-config-users.py
	install -m 0755 src/system-config-users $(DESTDIR)$(PKGDATADIR)
	install -m 0644 src/${PKGNAME}.glade $(DESTDIR)$(PKGDATADIR)
	install -m 0644 ${PKGNAME}.desktop $(DESTDIR)$(DATADIR)/applications/${PKGNAME}.desktop
	install -m 0644 ${PKGNAME}.pam $(DESTDIR)$(PAMD_DIR)/${PKGNAME}
	install -m 0644 ${PKGNAME}.console $(DESTDIR)$(SECURITY_DIR)/${PKGNAME}
	install -m 0644 ${PKGNAME}.prefs $(DESTDIR)$(SYSCONFIG_DIR)/${PKGNAME}
	install -m 0644 pixmaps/*.png $(DESTDIR)$(PKGDATADIR)
	ln -sf consolehelper $(DESTDIR)$(BINDIR)/${PKGNAME}
	for d in $(SUBDIRS); do \
	(cd $$d; $(MAKE) DESTDIR=$(DESTDIR) MANDIR=$(MANDIR) install) \
		|| case "$(MFLAGS)" in *k*) fail=yes;; *) exit 1;; esac; \
	done && test -z "$$fail"
	install -m 0644 man/system-config-users.8 $(DESTDIR)$(MANDIR)/man8/
	sleep 2
	python -c 'import compileall; compileall.compile_dir ("'"$(DESTDIR)$(PKGDATADIR)"'", ddir="'"$(PKGDATADIR)"'", maxlevels=10, force=1)'

clean: console-clean
	@rm -fv *~
	@rm -fv *.pyc
	@rm -fv system-config-user.desktop system-config-user.desktop.in.h
