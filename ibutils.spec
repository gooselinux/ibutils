#
# Copyright (c) 2006 Mellanox Technologies. All rights reserved.
#
# This Software is licensed under one of the following licenses:
#
# 3) under the terms of the "GNU General Public License (GPL) Version 2" a
#    copy of which is available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/gpl-license.php.
#
# Redistributions of source code must retain the above copyright
# notice and one of the license notices.
#
# Redistributions in binary form must reproduce both the above copyright
# notice, one of the license notices in the documentation
# and/or other materials provided with the distribution.
#
#
#  $Id: ibutils.spec.in 7656 2006-06-04 09:38:34Z vlad $
#

Summary: OpenIB Mellanox InfiniBand Diagnostic Tools
Name: ibutils
Version: 1.5.4
Release: 1%{?dist}
License: GPLv2 or BSD
Url: http://www.openfabrics.org/
Group: System Environment/Libraries
Source: http://www.openfabrics.org/downloads/%{name}/%{name}-%{version}.tar.gz
Patch0: ibutils-1.5.4-const.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: tcl, tk, swig
BuildRequires: libibverbs-devel >= 1.1, opensm-devel >= 3.3.0, tcl-devel, swig, tk, libibumad-devel, autoconf, libtool, graphviz-tcl
ExclusiveArch: i386 x86_64 ppc ia64
%description 
ibutils provides IB network and path diagnostics.

%package libs
Summary: Shared libraries used by ibutils binaries
Group: System Environment/Libraries
%description libs
Shared libraries used by the Mellanox Infiniband diagnostic utilities

%package devel
Summary: Development files to use the ibutils shared libraries
Group: System Environment/Libraries
Requires: ibutils-libs = %{version}-%{release}
%description devel
Headers and static libraries needed to develop applications that use
the Mellanox Infiniband diagnostic utilities libraries

%prep
%setup -q
#./autogen.sh
export CXXFLAGS="$CXXFLAGS -fno-strict-aliasing -fPIC"
export CFLAGS="$CFLAGS -fPIC"
%configure --with-osm=%{_prefix} --enable-ibmgtsim
%patch0 -p1 -b .const

%build
# The build isn't smp safe, so no %{?_smp_mflags}
make

%install
[ ! -z "$RPM_BUILD_ROOT" ] && rm -fr $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_bindir}/git_version.tcl
find $RPM_BUILD_ROOT -name \*.la | xargs rm
#rm -f $RPM_BUILD_ROOT%{_bindir}/ibdiagui
#rm -fr $RPM_BUILD_ROOT%{_libdir}/ibdiagui1.2
#rm -f $RPM_BUILD_ROOT%{_mandir}/man1/ibdiagui*

%clean
[ ! -z "$RPM_BUILD_ROOT" ] && rm -fr $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/ibis
%{_bindir}/ibdmsh
%{_bindir}/ibtopodiff
%{_bindir}/ibnlparse
%{_bindir}/ibdmtr
%{_bindir}/ibdmchk
%{_bindir}/ibdiagnet
%{_bindir}/ibdiagpath
%{_bindir}/ibdiagui
%{_bindir}/mkSimNodeDir
%{_bindir}/ibmssh
%{_bindir}/ibmsquit
%{_bindir}/RunSimTest
%{_bindir}/IBMgtSim
%{_datadir}/ibmgtsim
%{_mandir}/*/*

%files libs
%defattr(-,root,root)
%{_libdir}/libibdmcom.so.*
%{_libdir}/libibdm.so.*
%{_libdir}/libibmscli.so.*
%{_libdir}/libibsysapi.so.*
%dir %{_libdir}/ibis%{version}
%dir %{_libdir}/ibdm%{version}
%dir %{_libdir}/ibdiagnet%{version}
%dir %{_libdir}/ibdiagpath%{version}
%dir %{_libdir}/ibdiagui%{version}
%{_libdir}/ibis%{version}/*
%{_libdir}/ibdm%{version}/*
%{_libdir}/ibdiagnet%{version}/*
%{_libdir}/ibdiagpath%{version}/*
%{_libdir}/ibdiagui%{version}/*

%files devel
%defattr(-,root,root)
%{_libdir}/libibdmcom.so
%{_libdir}/libibdm.so
%{_libdir}/libibmscli.so
%{_libdir}/libibsysapi.so
%{_libdir}/libibdmcom.a
%{_libdir}/libibdm.a
%{_libdir}/libibmscli.a
%{_libdir}/libibsysapi.a
%{_includedir}/ibdm
%{_includedir}/ibmgtsim

%changelog
* Mon Mar 08 2010 Doug Ledford <dledford@redhat.com> - 1.5.4-1.el6
- Update to latest upstream version, which cleans up some licensing issues
  found in the previous versions during review
- Related: bz555835

* Mon Jan 25 2010 Doug Ledford <dledford@redhat.com> - 1.2-12.el6
- Update license for pkgwranger approval
- Related: bz543948

* Tue Dec 22 2009 Doug Ledford <dledford@redhat.com> - 1.2-11.el5
- Update to latest compatible upstream version
- Related: bz518218

* Fri Apr 17 2009 Doug Ledford <dledford@redhat.com> - 1.2-10
- Update to ofed 1.4.1-rc3 version
- Related: bz459652

* Tue Nov 11 2008 Doug Ledford <dledford@redhat.com> - 1.2-9
- Oops, forgot to remove the man page for ibdiagui, fix that
- Related: bz468122

* Mon Nov 10 2008 Doug Ledford <dledford@redhat.com> - 1.2-8
- Remove ibdiagui from the package entirely since it still doesn't work
  without graphviz-tcl
- Related: bz468122

* Thu Oct 23 2008 Doug Ledford <dledford@redhat.com> - 1.2-7
- Grab the upstream ibutils git repo, find a checkout that supports the
  recent opensm library versions and yet doesn't require graphviz-tcl,
  export that tree to a tarball with a git designation, build from it.
- Resolves: bz468122

* Thu Sep 18 2008 Doug Ledford <dledford@redhat.com> - 1.2-6
- Add a build flag to silence some compile warnings

* Wed Sep 17 2008 Doug Ledford <dledford@redhat.com> - 1.2-4
- Upstream has updated the tarball without changing the version number,
  grab the tarball from the OFED-1.4-beta1 tarball and use it.
- Resolves: bz451467

* Tue Jan 29 2008 Doug Ledford <dledford@redhat.com> - 1.2-3
- Bump and rebuild against OFED 1.3 libraries
- Resolves: bz428198

* Wed Jun 27 2007 Doug Ledford <dledford@redhat.com> - 1.2-2
- Bump and rebuild against openib-1.2 libraries

* Mon Jun 25 2007 Doug Ledford <dledford@redhat.com> - 1.2-1
- Update to OFED 1.2 released package
- Related: bz245817

* Wed Oct 25 2006 Tim Powers <timp@redhat.com> - 1.0-3
- rebuild against openib package set due to soname change

* Fri Oct 20 2006 Doug Ledford <dledford@redhat.com>
- Bump and rebuild against latest openib packages
- Disable ibmgtsim until I can figure out why it's failing to wrap a
  perfectly existent library function (I hate c++)

* Mon Jul 31 2006 Doug Ledford <dledford@redhat.com> 1.0-2
- Make spec file name convention/multilib compliant
- Move all the files to FHS compliant locations for a distributor

* Tue May 16 2006 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Added ibutils sh, csh and conf to update environment

* Sun Apr  2 2006 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Initial packaging for openib gen2 stack
