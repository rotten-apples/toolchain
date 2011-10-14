# FIXME: This would attempt to strip target platform .a files
%global __spec_install_post %{nil}
%global debug_package %{nil}

%global _target arm-apple-darwin10
%global _program_prefix %{_target}-

%global apple_build 5666.3

Name:           %{_program_prefix}gcc
Version:        4.2.1
Release:        1.%{apple_build}%{?dist}
Summary:        Cross-compiler for iOS

Group:          Development/Languages
License:        GPLv2+
URL:            http://www.opensource.apple.com/
Source0:        http://www.opensource.apple.com/tarballs/gcc/gcc-%{apple_build}.tar.gz
Patch1:         0001-Apply-gcc_42-5574.patch.patch
Patch2:         0002-Add-arm.patch
Patch3:         0003-Only-build-arm-v6.patch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  cctools
BuildRequires:  %{_target}-sdk
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  gettext

Requires:       cctools
Requires:       %{_target}-sdk

AutoProv:       0

%description
This is the cross-compiler for Apple Darwin on ARM ("iOS") platform.
It's based upon compiler source released by Apple enhanced by numerous
free software developers.


%prep
%setup -q -n gcc-%{apple_build}
%patch1 -p1
%patch2 -p1
%patch3 -p1


%build
mkdir -p gcc-%{version}-build
cd gcc-%{version}-build
%define _configure ../configure
# %%configure would set --build which causes CFLAGS to be
# used for libstdc++ for some reason
%_configure --target=%{_target} \
        --prefix=%{_prefix} \
        --disable-checking \
        --enable-languages=c,objc,c++,obj-c++ \
        --mandir=%{_mandir} \
        --with-ld=%{_bindir}/ld64 \
        --with-sysroot=/usr/arm-apple-darwin10
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make -C gcc-%{version}-build install DESTDIR=$RPM_BUILD_ROOT

# XXX
mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{_target}%{_libdir}
ln -s ../../../..%{_libdir}/gcc $RPM_BUILD_ROOT%{_prefix}/%{_target}%{_libdir}/

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/%{_program_prefix}*
%{_prefix}/%{_target}
%{_libexecdir}/*
%{_libdir}/gcc
%{_mandir}/man1/%{_program_prefix}*
%exclude %{_mandir}/man7
%exclude %{_datadir}/locale
%exclude %{_libdir}/libiberty.a
%doc CHANGES.Apple
%doc COPYING*
%doc README*


%changelog
