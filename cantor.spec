
# omit until R FTBFS is fixed, https://bugzilla.redhat.com/742234
%if 0%{?fedora} < 17
%define R_support 1
%endif

Name:    cantor 
Summary: KDE Frontend to Mathematical Software 
Version: 4.7.2
Release: 1%{?dist}

License: GPLv2+
URL:     https://projects.kde.org/projects/kde/kdeedu/cantor
Source0: http://download.kde.org/stable/%{version}/src/%{name}-%{version}.tar.bz2

BuildRequires: desktop-file-utils
BuildRequires: kdelibs4-devel >= %{version}
BuildRequires: pkgconfig(eigen2)
BuildRequires: pkgconfig(libspectre)
%if 0%{?R_support}
BuildRequires: pkgconfig(libR)
%else
Obsoletes: kdeedu-math-cantor-R < 4.7.0-10
Obsoletes: %{name}-R < %{version}-%{release}
%endif

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: kdebase-runtime%{?_kde4_version: >= %{_kde4_version}}

%description
%{summary}.

%package  libs
Summary:  Runtime files for %{name}
# when split occurred
Conflicts: kdeedu-math-libs < 4.7.0-10
Requires: %{name} = %{version}-%{release}
%description libs
%{summary}.

%package R
Summary: R backend for %{name}
Obsoletes: kdeedu-math-cantor-R < 4.7.0-10
Provides:  kdeedu-math-cantor-R = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description R 
%{summary}.

%package devel
Summary:  Development files for %{name}
# when split occurred
Conflicts: kdeedu-devel < 4.7.0-10
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: kdelibs4-devel
%description devel
%{summary}.


%prep
%setup -q


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name} --with-kde --without-mo


%check
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/cantor.desktop


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
fi

%files -f %{name}.lang
%doc COPYING COPYING.DOC
%doc README TODO
%{_kde4_bindir}/cantor
%{_kde4_datadir}/applications/kde4/cantor.desktop
%{_kde4_datadir}/config.kcfg/cantor.kcfg
%{_kde4_datadir}/config.kcfg/cantor_libs.kcfg
%{_kde4_datadir}/config.kcfg/maximabackend.kcfg
%{_kde4_datadir}/config.kcfg/octavebackend.kcfg
%{_kde4_datadir}/config.kcfg/sagebackend.kcfg
%{_kde4_configdir}/cantor.knsrc
%{_kde4_configdir}/cantor_kalgebra.knsrc
%{_kde4_configdir}/cantor_maxima.knsrc
%{_kde4_configdir}/cantor_sage.knsrc
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_appsdir}/cantor/
%{_kde4_datadir}/kde4/servicetypes/cantor_*.desktop
%{_kde4_libdir}/kde4/cantor_*.so
%{_kde4_datadir}/kde4/services/cantor/
%if 0%{?R_support}
%exclude %{_kde4_libdir}/kde4/cantor_rbackend.so
%exclude %{_kde4_datadir}/kde4/services/cantor/rbackend.desktop

%files R
%{_kde4_bindir}/cantor_rserver
%{_kde4_libdir}/kde4/cantor_rbackend.so
%{_kde4_datadir}/config.kcfg/rserver.kcfg
%{_kde4_configdir}/cantor_r.knsrc
%{_kde4_datadir}/kde4/services/cantor/rbackend.desktop
%endif

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_kde4_libdir}/kde4/libcantorpart.so
%{_kde4_libdir}/libcantorlibs.so.*
%{_kde4_libdir}/libcantor_config.so

%files devel
%{_kde4_includedir}/cantor/
%{_kde4_libdir}/libcantorlibs.so


%changelog
* Wed Oct 05 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-1
- 4.7.2

* Wed Sep 21 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-2
- License: GPLv2+
- %%doc COPYING

* Sat Sep 17 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-1
- 4.7.1

* Tue Aug 30 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.0-10
- first try

