Summary:	Communication library between internal components for Ultimaker software
Name:		libArcus
Version:	2.5.0
Release:	2
License:	AGPLv3+
Group:		Libraries
URL:		https://github.com/Ultimaker/libArcus
Source0:	https://github.com/Ultimaker/libArcus/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a8f83c896793262967971b7a94fe3082
BuildRequires:	cmake
BuildRequires:	libstdc++-devel
BuildRequires:	protobuf-devel
BuildRequires:	python3-devel
BuildRequires:	python3-protobuf
BuildRequires:	python3-sip-devel
BuildRequires:	sip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Arcus library contains C++ code and Python 3 bindings for creating a
socket in a thread and using this socket to send and receive messages
based on the Protocol Buffers library. It is designed to facilitate
the communication between Cura and its backend and similar code.

%package        devel
Summary:	Development files for libArcus
License:	AGPLv3+ and BSD
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description    devel
Arcus library contains C++ code and Python 3 bindings for creating a
socket in a thread and using this socket to send and receive messages
based on the Protocol Buffers library. It is designed to facilitate
the communication between Cura and its backend and similar code.

Development files.

%package -n     python3-Arcus
Summary:	Python 3 libArcus bindings
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-Arcus
Arcus Python 3 bindings for creating a socket in a thread and using
this socket to send and receive messages based on the Protocol Buffers
library. It is designed to facilitate the communication between Cura
and its backend and similar code.

%prep
%setup -q

%build
mkdir build
cd build
%{cmake} .. \
	-DPYTHON_SITE_PACKAGES_DIR:PATH=%{py3_sitedir} \
	-DBUILD_EXAMPLES:BOOL=OFF \
	-DCMAKE_SKIP_RPATH:BOOL=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755, root, root) %{_libdir}/libArcus.so.*.*.*
%attr(755, root, root) %ghost %{_libdir}/libArcus.so.3

%files devel
%defattr(644,root,root,755)
%doc examples/example.cpp examples/example.proto
%attr(755, root, root) %{_libdir}/libArcus.so
%{_includedir}/Arcus
%{_libdir}/cmake/Arcus

%files -n python3-Arcus
%defattr(644,root,root,755)
%doc TODO.md
%doc examples/example.py
%attr(755, root, root) %{py3_sitedir}/Arcus.so
