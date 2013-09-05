Name:    cantor 
Summary: KDE Frontend to Mathematical Software 
Version: 4.10.4
Release: 2%{?dist}

License: GPLv2+
URL:     https://projects.kde.org/projects/kde/kdeedu/cantor
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/%{version}/src/%{name}-%{version}.tar.xz

## upstream patches
# fix SAGE backend for SAGE 5.8 (kde#316299), from master/4.11
Patch100: cantor-4.10.4-sage58.patch

BuildRequires: analitza-devel >= %{version}
BuildRequires: desktop-file-utils
BuildRequires: kdelibs4-devel >= %{version}
BuildRequires: pkgconfig(eigen2)
BuildRequires: pkgconfig(libqalculate)
BuildRequires: pkgconfig(libR)
BuildRequires: pkgconfig(libspectre)

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: kde-runtime%{?_kde4_version: >= %{_kde4_version}}
Requires: kate-part%{?_kde4_version: >= %{_kde4_version}}

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
%patch100 -p1 -b .sage58


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
%{_kde4_datadir}/config.kcfg/qalculatebackend.kcfg
%{_kde4_datadir}/config.kcfg/sagebackend.kcfg
%{_kde4_datadir}/config.kcfg/scilabbackend.kcfg
%{_kde4_configdir}/cantor.knsrc
%{_kde4_configdir}/cantor_kalgebra.knsrc
%{_kde4_configdir}/cantor_maxima.knsrc
%{_kde4_configdir}/cantor_sage.knsrc
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_appsdir}/cantor/
%{_kde4_datadir}/kde4/servicetypes/cantor_*.desktop
%{_kde4_libdir}/kde4/cantor_*.so
%{_kde4_datadir}/kde4/services/cantor/
%exclude %{_kde4_libdir}/kde4/cantor_rbackend.so
%exclude %{_kde4_datadir}/kde4/services/cantor/rbackend.desktop

%files R
%{_kde4_bindir}/cantor_rserver
%{_kde4_libdir}/kde4/cantor_rbackend.so
%{_kde4_datadir}/config.kcfg/rserver.kcfg
%{_kde4_configdir}/cantor_r.knsrc
%{_kde4_datadir}/kde4/services/cantor/rbackend.desktop

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
* Sat Jun 29 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.10.4-2
- update the SAGE 5.8 patch to the version committed to master/4.11

* Sat Jun 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.4-1
- 4.10.4

* Sun May 26 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.10.3-2
- fix SAGE backend for SAGE 5.8 (kde#316299), patch from upstream bugs.kde.org

* Mon May 06 2013 Than Ngo <than@redhat.com> - 4.10.3-1
- 4.10.3

* Sun Mar 31 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-1
- 4.10.2

* Sat Mar 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.1-1
- 4.10.1

* Thu Feb 07 2013 Rex Dieter <rdieter@fedoraproject.org> 4.10.0-2
- recent libgfortran-related commits breaks cantor-R support (kde#314253)

* Fri Feb 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.0-1
- 4.10.0

* Tue Jan 22 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.98-1
- 4.9.98

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.97-1
- 4.9.97

* Thu Dec 20 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.95-1
- 4.9.95

* Tue Dec 04 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.90-1
- 4.9.90

* Mon Dec 03 2012 Than Ngo <than@redhat.com> - 4.9.4-1
- 4.9.4

* Sat Nov 03 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.3-1
- 4.9.3

* Sat Sep 29 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-1
- 4.9.2

* Mon Sep 03 2012 Than Ngo <than@redhat.com> - 4.9.1-1
- 4.9.1

* Thu Jul 26 2012 Lukas Tinkl <ltinkl@redhat.com> - 4.9.0-1
- 4.9.0

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.97-1
- 4.8.97

* Wed Jun 27 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.95-1
- 4.8.95

* Sat Jun 09 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.90-1
- 4.8.90

* Fri Jun 01 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.80-1
- 4.8.80

* Mon Apr 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.3-1
- 4.8.3

* Fri Mar 30 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-1
- 4.8.2

* Mon Mar 05 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.1-1
- 4.8.1

* Sun Jan 22 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.0-1
- 4.8.0

* Wed Jan 04 2012 Radek Novacek <rnovacek@redhat.com> - 4.7.97-1
- 4.7.97

* Thu Dec 22 2011 Radek Novacek <rnovacek@redhat.com> - 4.7.95-1
- 4.7.95

* Sun Dec 04 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.7.90-1
- 4.7.90

* Sat Dec 03 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.80-2
- BR: analitza-devel pkgconfig(libqalculate) 

* Fri Nov 25 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.80-1
- 4.7.80

* Wed Nov  9 2011 Tom Callaway <spot@fedoraproject.org> 4.7.3-2
- rebuild for R 2.14.0

* Sat Oct 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.3-1
- 4.7.3

* Sat Oct 08 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-3
- Requires: kate-part

* Sat Oct 08 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7.2-2
- restore R support (unconditionally, was temporarily disabled on F17+)

* Wed Oct 05 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-1
- 4.7.2

* Wed Sep 21 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-2
- License: GPLv2+
- %%doc COPYING

* Sat Sep 17 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-1
- 4.7.1

* Tue Aug 30 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.0-10
- first try

