Name: hesiod
Version: 3.0.2
Release: 15
Source: ftp://athena-dist.mit.edu/pub/ATHENA/hesiod/hesiod-%{version}.tar.gz
Patch0: hesiod-3.0.2-shlib.patch
Patch1: hesiod-3.0.2-env.patch
Patch2: hesiod-3.0.2-str.patch
Summary: Hesiod libraries and sample programs.
Group: System Environment/Libraries
License: MIT
Buildroot: %{_tmppath}/hesiod-root

%description
Hesiod is a system which uses existing DNS functionality to provide access
to databases of information that changes infrequently.  It is often used to
distribute information kept in the /etc/passwd, /etc/group, and /etc/printcap
files, among others.

%package devel
Summary: Development libraries and headers for Hesiod
Group: Development/Libraries
Requires: hesiod = %{version}-%{release}

%description devel
Hesiod is a system which uses existing DNS functionality to provide access
to databases of information that changes infrequently.  It is often used to
distribute information which might otherwise kept in the /etc/passwd,
/etc/group, and /etc/printcap files over a network, eliminating the need to
ensure synchronize the files among multiple hosts.  This package contains
the header files and libraries required for building programs which use Hesiod.

%changelog
* Fri Oct 26 2001 Nalin Dahyabhai <nalin@redhat.com> 3.0.2-15
- actually set the soname in the shared library (ld doesn't automatically
  set the soname to the output file's name, oops)

* Fri Oct  5 2001 Nalin Dahyabhai <nalin@redhat.com> 3.0.2-14
- on second thought, put the shared library back in, using a soversion of 0
  to have a chance at providing compatibility with apps linked dynamically
  on other distributions
- make -devel depend on the same version of the main package

* Wed Oct  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- remove the shared library patch -- different packages with shared libraries
  tend to use different sonames, so we'd run inevitably run into problems

* Thu Aug 21 2001 Nalin Dahyabhai <nalin@redhat.com>
- remove pre and post scripts -- authconfig handles that stuff now
- add the hesiod man page back in, as bind-devel doesn't provide it any more

* Wed Jan 17 2001 Jeremy Katz <jlkatz@eos.ncsu.edu>
- hesiod-devel requires hesiod (bug #128)

* Thu Sep 14 2000 Jeremy Katz <jlkatz@eos.ncsu.edu>
- remove hesiod man page from hesiod-devel as it conflicts with the one 
  from bind-devel

* Thu Sep 14 2000 Jeremy Katz <jlkatz@eos.ncsu.edu>
- use rpm macros where possible and FHS-ify
- split into main and devel packages
- add back requires for nscd

* Fri Jul 28 2000 Jeremy Katz <jlkatz@eos.ncsu.edu>
- rebuild in new environment

* Thu Mar 16 2000 Jeremy Katz <jlkatz@unity.ncsu.edu>
- rebuild in new environment

* Thu Sep  2 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- removed dependency on nscd
- changed requires: nscd back to caching-nameserver

* Mon May 17 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- started changelog
- moved addition of hesiod to nsswitch.conf to this package because we
  no longer use a separate libnss_hesiod.so
- changed requires: caching-nameserver to nscd
- added post-install script snippet to activate nscd on install

%prep
%setup -q
%patch0 -p1 -b .shlib
%patch1 -p1 -b .env
%patch2 -p1 -b .str
for manpage in *.3; do
	if grep -q '^\.so man3/hesiod.3' $manpage ; then
		echo .so hesiod.3 > $manpage
	elif grep -q '^\.so man3/hesiod_getmailhost.3' $manpage ; then
		echo .so hesiod_getmailhost.3 > $manpage
	elif grep -q '^\.so man3/hesiod_getpwnam.3' $manpage ; then
		echo .so hesiod_getpwnam.3 > $manpage
	elif grep -q '^\.so man3/hesiod_getservbyname.3' $manpage ; then
		echo .so hesiod_getservbyname.3 > $manpage
	fi
done

%build
%configure 
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%makeinstall

%files
%defattr(-,root,root)
%doc README NEWS
%{_bindir}/hesinfo
%{_libdir}/libhesiod.so.*
%{_mandir}/man1/*
%{_mandir}/man5/*

%files devel
%defattr(-,root,root)
%{_libdir}/libhesiod.a
%{_libdir}/libhesiod.so
%{_includedir}/hesiod.h
%{_mandir}/man3/*
