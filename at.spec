Summary: Job spooling tools.
Name: at
Version: 3.1.8
Release: 23
License: GPL
Group: System Environment/Daemons
Source: ftp://tsx-11.mit.edu/pub/linux/sources/usr.bin/at-3.1.8.tar.bz2
Source2: atd.init
Patch0: at-3.1.7-lockfile.patch
Patch1: at-3.1.7-noon.patch
Patch2: at-3.1.7-paths.patch
Patch3: at-3.1.7-sigchld.patch
Patch4: at-noroot.patch
Patch5: at-3.1.7-typo.patch
Patch6: at-debian.patch
Patch7: at-3.1.8-buflen.patch
Patch9: at-3.1.8-shell.patch
Patch10: at-3.1.8-batch.patch
Patch11: at-3.1.8-lexer.patch
Patch12: at-3.1.8-dst.patch
Patch13: at-3.1.8-test.patch
Patch14: at-3.1.8-test-fix.patch
#Patch15: at-3.1.8-env.patch
Patch15: at-3.1.8-env-tng.patch
Patch16: at-3.1.8-lsbdoc.patch
Patch17: at-3.1.8-o_excl.patch
Prereq: fileutils chkconfig /etc/init.d
BuildPrereq: flex bison autoconf
Conflicts: crontabs <= 1.5
# No, I'm not kidding
BuildPrereq: sendmail
Buildroot: %{_tmppath}/%{name}-root

%description
At and batch read commands from standard input or from a specified
file. At allows you to specify that a command will be run at a
particular time. Batch will execute commands when the system load
levels drop to a particular level. Both commands use /bin/sh.

You should install the at package if you need a utility for
time-oriented job control. Note: If it is a recurring job that will
need to be repeated at the same time every day/week, etc. you should
use crontab instead.

%prep
%setup -q
%patch0 -p1 -b .lockfile
# The next path is a brute-force fix that will have to be updated
# when new versions of at are released.
%patch2 -p1 -b .paths

%patch3 -p1 -b .sigchld
%patch6 -p1 -b .debian
%patch4 -p1 -b .noroot
%patch5 -p1 -b .tyop
%patch7 -p1 -b .buflen
%patch9 -p1 -b .shell
%patch10 -p1 -b .batch
%patch11 -p1 -b .lexer
%patch12 -p1 -b .dst
%patch13 -p1 -b .test
%patch14 -p1 -b .test-fix
%patch15 -p1 -b .env
%patch16 -p1 -b .lsbdoc
%patch17 -p1 -b .o_excl

%build
# for patch 9
autoconf
%configure --with-atspool=/var/spool/at/spool --with-jobdir=/var/spool/at

# for patch 11
rm -f lex.yy.* y.tab.*

make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc/rc.d/init.d

%makeinstall DAEMON_USERNAME=`id -nu` \
	DAEMON_GROUPNAME=`id -ng` \
	etcdir=%{buildroot}/etc \
	ATJOB_DIR=%{buildroot}/var/spool/at \
	ATSPOOL_DIR=%{buildroot}/var/spool/at/spool 
echo > %{buildroot}/etc/at.deny
mkdir docs
cp $RPM_BUILD_ROOT/%{_prefix}/doc/at/* docs/
install -m 755 %{SOURCE2} %{buildroot}/etc/rc.d/init.d/atd

mv -f %{buildroot}/%{_mandir}/man5/at_allow.5 \
      %{buildroot}/%{_mandir}/man5/at.allow.5
rm -f %{buildroot}/%{_mandir}/man5/at_deny.5
ln -s at.allow.5 \
      %{buildroot}/%{_mandir}/man5/at.deny.5

%clean
rm -rf %{buildroot}

%post
touch /var/spool/at/.SEQ
chmod 600 /var/spool/at/.SEQ
chown daemon.daemon /var/spool/at/.SEQ
/sbin/chkconfig --add atd

%preun
if [ "$1" = 0 ] ; then
  service atd stop >/dev/null 2>&1
  /sbin/chkconfig --del atd
fi

%postun
if [ "$1" -ge "1" ]; then
  service atd condrestart >/dev/null 2>&1
fi

%files
%defattr(-,root,root)
%doc docs/*
%config /etc/at.deny
%config /etc/rc.d/init.d/atd
%attr(0700,daemon,daemon)	%dir /var/spool/at
%attr(0600,daemon,daemon)	%verify(not md5 size mtime) %ghost /var/spool/at/.SEQ
%attr(0700,daemon,daemon)	%dir /var/spool/at/spool
%{_prefix}/sbin/atrun
%{_prefix}/sbin/atd
%{_mandir}/man*/*
%{_prefix}/bin/batch
%{_prefix}/bin/atrm
%{_prefix}/bin/atq
%attr(4755,root,root)	%{_prefix}/bin/at

%changelog
* Thu Jan 17 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.1.8-23
- s/Copyright/License/

* Mon Jan 14 2002 Adrian Havill <havill@redhat.com> 3.1.8-21
- fix man page (#51253)
- fix env prop problem (#49491)
- .SEQ should not be executable (#52626)
- beefed up file creation perms against symlink exploits (O_EXCL)

* Thu Aug  2 2001 Crutcher Dunnavant <crutcher@redhat.com> 3.1.8-20
- updated patch update, still bug #46546

* Mon Jul 18 2001 Crutcher Dunnavant <crutcher@redhat.com>
- applied enrico.scholz@informatik.tu-chemnitz.de's change to the env patch to 
- address bug #46546

* Mon Jun 25 2001 Crutcher Dunnavant <crutcher@redhat.com>
- changed atd.init to start at 95, stop at 5, closing #15915
- applied mailto:wp@supermedia.pl's environment patch

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Apr  4 2001 Crutcher Dunnavant <crutcher@redhat.com>
- much love to David Kilzer <ddkilzer@lubricants-oil.com>
- who nailed UTC, Leap year, DST, and some other edge cases down
- he also wrote a test harness in perl
- bug #28448

* Fri Feb  2 2001 Trond Eivind Glomsrød <teg@redhat.com>
- i18nize initscript

* Wed Dec 12 2000 Bill Nottingham <notting@redhat.com>
- fix documentation of which shell commands will be run with (#22216)

* Wed Aug 23 2000 Crutcher Dunnavant <crutcher@redhat.com>
- Well, we will likely never really close the UTC issues,
- because of 1) fractional timezones, and 2) daylight savigns time.
- but there is a slight tweak to the handling of dst in the UTC patch.

* Wed Aug 23 2000 Crutcher Dunnavant <crutcher@redhat.com>
- fixed bug #15685
- which had at miscaluclating UTC times.

* Sat Jul 15 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jul  6 2000 Bill Nottingham <notting@redhat.com>
- prereq /etc/init.d

* Sat Jul  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix syntax error in init script

* Tue Jun 27 2000 Preston Brown <pbrown@redhat.com>
- don't prereq, only require initscripts

* Mon Jun 26 2000 Preston Brown <pbrown@redhat.com>
- move init script
- add condrestart directive
- fix post/preun/postun scripts
- prereq initscripts >= 5.20

* Sat Jun 17 2000 Bill Nottingham <notting@redhat.com>
- fix verify of /var/spool/at/.SEQ (#12262)

* Mon Jun 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix status checking and syntax error in init script

* Fri Jun  9 2000 Bill Nottingham <notting@redhat.com>
- fix for long usernames (#11321)
- add some bugfixes from debian

* Mon May  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 3.1.8

* Wed Mar  1 2000 Bill Nottingham <notting@redhat.com>
- fix a couple of more typos, null-terminate some strings

* Thu Feb 10 2000 Bill Nottingham <notting@redhat.com>
- fix many-years-old typo in atd.c

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging, build as non-root user

* Sun Jun 13 1999 Jeff Johnson <jbj@redhat.com>
- correct perms for /var/spool/at after defattr.

* Mon May 24 1999 Jeff Johnson <jbj@redhat.com>
- reset SIGCHLD before exec (#3016).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 8)

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- fix handling the 12:00 time

* Wed Jan 13 1999 Bill Nottingham <notting@redhat.com>
- configure fix for arm

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 22 1998 Michael K. Johnson <johnsonm@redhat.com>
- enhanced initscript

* Sun Nov 09 1997 Michael K. Johnson <johnsonm@redhat.com>
- learned to spell

* Wed Oct 22 1997 Michael K. Johnson <johnsonm@redhat.com>
- updated to at version 3.1.7
- updated lock and sequence file handling with %ghost
- Use chkconfig and atd, now conflicts with old crontabs packages

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc

