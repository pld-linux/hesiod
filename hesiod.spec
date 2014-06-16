Summary:	Hesiod libraries and sample programs
Summary(pl.UTF-8):	Biblioteki i programy przykładowe do hesiod
Name:		hesiod
Version:	3.2.1
Release:	1
License:	BSD
Group:		Libraries
Source0:	ftp://athena-dist.mit.edu/pub/ATHENA/hesiod/%{name}-%{version}.tar.gz
# Source0-md5:	d8fe6d7d081c9c14d5d3d8a466998eeb
BuildRequires:	libidn-devel
BuildRequires:	sed >= 4.0
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
Requires:	libidn-devel

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

grep -l '^\.so man3/' man/*.3 | xargs %{__sed} -i -e '1s,man3/,,;2,$d'

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libhesiod.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING NEWS README
%attr(755,root,root) %{_bindir}/hesinfo
%attr(755,root,root) %{_libdir}/libhesiod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhesiod.so.0
%{_mandir}/man1/hesinfo.1*
%{_mandir}/man5/hesiod.conf.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhesiod.so
%{_includedir}/hesiod.h
%{_pkgconfigdir}/hesiod.pc
%{_mandir}/man3/hesiod*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libhesiod.a
