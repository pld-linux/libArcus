Summary:	Communication library between internal components for Ultimaker software
Summary(pl.UTF-8):	Biblioteka komunikacji między wewnętrznymi komponentami oprogramowania Ultimaker
Name:		libArcus
Version:	4.5.0
Release:	2
License:	AGPL v3+
Group:		Libraries
#Source0Download: https://github.com/Ultimaker/libArcus/releases
Source0:	https://github.com/Ultimaker/libArcus/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2966fc6e19f0ace9803cc90754a5f0fd
Patch0:		PyQt5-sip.patch
URL:		https://github.com/Ultimaker/libArcus
BuildRequires:	cmake >= 2.8.12
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	protobuf-devel >= 3.0.0
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-sip-devel
BuildRequires:	sip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Arcus library contains C++ code and Python 3 bindings for creating a
socket in a thread and using this socket to send and receive messages
based on the Protocol Buffers library. It is designed to facilitate
the communication between Cura and its backend and similar code.

%description -l pl.UTF-8
Biblioteka Arcus zawiera kod C++ oraz wiązania Pythona 3 do tworzenia
gniazda w wątku i wykorzystywania tego gniazda do wysyłania i
odbierania komunikatów w oparciu o bibliotekę Protocol Buffers.
Została zaprojektowana, aby ułatwić komunikację między programem Cura
a jego backendem i podobnym kodem.

%package devel
Summary:	Development files for libArcus
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libArcus
License:	AGPL v3+ and BSD
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for libArcus.

%description devel -l pl
Pliki programistyczne biblioteki libArcus.

%package -n python3-Arcus
Summary:	Python 3 bindings for libArcus
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki libArcus
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-Arcus
Arcus Python 3 bindings for creating a socket in a thread and using
this socket to send and receive messages based on the Protocol Buffers
library. It is designed to facilitate the communication between Cura
and its backend and similar code.

%description -n python3-Arcus -l pl.UTF-8
Wiązania Pythona 3 do biblioteki Arcus, tworzącej gniazdo w wątku i
wykorzystującej to gniazdo do wysyłania i odbierania komunikatów w
oparciu o bibliotekę Protocol Buffers. Biblioteka została
zaprojektowana, aby ułatwić komunikację między programem Cura a jego
backendem i podobnym kodem.

%prep
%setup -q
%patch0 -p1

%build
mkdir build
cd build
%cmake .. \
	-DBUILD_EXAMPLES:BOOL=OFF \
	-DCMAKE_SKIP_RPATH:BOOL=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{py3_sitedir}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# python location detection is totally screwed in this package
%{__mv} $RPM_BUILD_ROOT{/usr/local/%{_lib}/python3*/site-packages,%{py3_sitedir}}/Arcus.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md TODO.md
%attr(755,root,root) %{_libdir}/libArcus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libArcus.so.3

%files devel
%defattr(644,root,root,755)
%doc examples/example.cpp examples/example.proto
%attr(755,root,root) %{_libdir}/libArcus.so
%{_includedir}/Arcus
%{_libdir}/cmake/Arcus

%files -n python3-Arcus
%defattr(644,root,root,755)
%doc examples/example.py
%attr(755,root,root) %{py3_sitedir}/Arcus.so
