Summary:	Hesiod libraries and sample programs
Summary(pl.UTF-8):	Biblioteki i programy przykładowe do hesiod
Name:		hesiod
Version:	3.0.2
Release:	15
License:	MIT
Source0:	ftp://athena-dist.mit.edu/pub/ATHENA/hesiod/%{name}-%{version}.tar.gz
# Source0-md5:	0362311e80fb1e029a1588cbbd09ad57
Patch0:		%{name}-3.0.2-shlib.patch
Patch1:		%{name}-3.0.2-env.patch
Patch2:		%{name}-3.0.2-str.patch
Group:		Libraries
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hesiod is a system which uses existing DNS functionality to provide
access to databases of information that changes infrequently. It is
often used to distribute information kept in the /etc/passwd,
/etc/group, and /etc/printcap files over a network, eliminating the
need to ensure synchronize the files among multiple hosts.

%description -l pl.UTF-8
Hesiod jest systemem używającym istniejącej funkcjonalności DNS do
zapewniania dostępu do baz informacji zmieniających się niezbyt
często. Jest przeważnie używany do rozprowadzania informacji
trzymanych w /etc/passwd, /etc/group, /etc/printcap i podobnych po
sieci, eliminując potrzebę synchronizacji plików między wieloma
komputerami.

%package devel
Summary:	Headers and development documentation for Hesiod
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja programisty do hesiod
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files required for building programs
which use Hesiod and some devolopment documentation.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do budowania programów
używających Hesiod oraz dokumentację programisty.

%package static
Summary:	Hesiod static library
Summary(pl.UTF-8):	Biblioteka statyczna Hesiod
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static version of Hesiod library.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczną wersję biblioteki Hesiod.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

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
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README NEWS
%attr(755,root,root) %{_bindir}/hesinfo
%attr(755,root,root) %{_libdir}/libhesiod.so.*
%{_mandir}/man1/*
%{_mandir}/man5/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhesiod.so
%{_includedir}/hesiod.h
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/libhesiod.a
