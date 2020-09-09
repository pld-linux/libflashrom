#
# Conditional build:
%bcond_without	apidocs	# API documentation

%ifarch %{ix86} %{x8664} x32
%define		with_pci_io	1
%endif

Summary:	Flash ROM programming library
Summary(pl.UTF-8):	Biblioteka do programowania pamięci Flash ROM
Name:		libflashrom
Version:	0
%define	gitref	cdaebf16a766be01f8f3dfe17c05bc6626da2964
%define	snap	20190207
%define	rel	1
Release:	0.%{snap}.1
License:	GPL v2+
Group:		Libraries
# releases? (currently only a copy of flashrom releases) https://github.com/fwupd/flashrom/releases
# branch https://github.com/fwupd/flashrom/commits/wip/hughsie/fwupd
Source0:	https://github.com/fwupd/flashrom/archive/%{gitref}/flashrom-%{snap}.tar.gz
# Source0-md5:	f54475af56c26dd584f804aad4ed708f
URL:		https://github.com/fwupd/flashrom
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	gcc >= 5:3.2
BuildRequires:	libftdi1-devel >= 1.0
BuildRequires:	libusb-compat-devel >= 0.1
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	meson >= 0.47.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pciutils-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Flash ROM programming library.

%description -l pl.UTF-8
Biblioteka do programowania pamięci Flash ROM.

%package devel
Summary:	Header files for libflashrom library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libflashrom
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libflashrom library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libflashrom.

%package apidocs
Summary:	API documentation for libflashrom library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libflashrom
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for libflashrom library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libflashrom.

%prep
%setup -q -n flashrom-%{gitref}

%build
%meson build \
%if %{without pci_io}
	-Dconfig_nic3com=false \
	-Dconfig_nicrealtek=false \
	-Dconfig_rayer_spi=false \
	-Dconfig_satamv=false
%endif

%ninja_build -C build

%if %{with apidocs}
doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README Documentation/*.txt
%attr(755,root,root) %{_libdir}/libflashrom.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libflashrom.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libflashrom.so
%{_includedir}/libflashrom.h
%{_pkgconfigdir}/libflashrom.pc

%if 0
# is it stable enough to obsolete one from flashrom.spec?
%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/flashrom
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc libflashrom-doc/html/{search,*.css,*.html,*.js,*.png}
%endif
