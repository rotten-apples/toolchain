Name:           cctools
Version:        795
Release:        1%{?dist}
Summary:        Compiler helper tools from Darwin

Group:          Development/Tools
License:        APSL
URL:            http://www.opensource.apple.com/release/ios-433/

# cctools bundle
Source0:        http://www.opensource.apple.com/tarballs/%{name}/%{name}-%{version}.tar.gz
Patch1:         0001-Import-http-toolwhip.googlecode.com-svn-trunk-cctool.patch
Patch2:         0002-Always-set-archive-mtime-to-0.patch
Patch3:         0003-Do-not-grok-objc-ABI-in-otool.patch
Patch4:         0004-Drop-unused-symbol.patch
Patch5:         0005-Drop-ppc64-support.patch
Patch6:         0006-Includedir.patch
Patch7:         0007-Enable-arm.patch
Patch8:         0008-Fix-FORTIFY_SOURCE-crashes.patch
Patch9:         0009-Fix-ranlib-discovery.patch

# Additional tools that did not fit elsewhere
# http://networkpx.googlecode.com/svn/etc/dyldcache.cc@515
Source1:        http://networkpx.googlecode.com/svn/etc/dyldcache.cc

BuildRequires:  gcc-objc
BuildRequires:  xnu-headers
BuildRequires:  libuuid-devel
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# Certain parts hardcoded to -D__LITTLE_ENDIAN__
# in SPEC and in Makefiles
ExclusiveArch:  %{ix86} x86_64

%description
A collection of utilities that supplement the compiler, including the
assembler and linker.


%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
cp %{SOURCE1} dyldcache.cc


%build
make -f Makefile.linux CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
g++ -I/usr/include/xnu -D__LITTLE_ENDIAN__ -o dyldcache dyldcache.cc


%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
for T in                        \
        misc/strip              \
        misc/codesign_allocate  \
        misc/libtool            \
        misc/nm                 \
        misc/install_name_tool  \
        misc/size               \
        misc/pagestuff          \
        misc/segedit            \
        misc/nmedit             \
        misc/strings            \
        misc/lipo               \
        as/bin/as               \
        ld/ld_classic           \
        otool/otool             \
        ar/ar                   \
        dyldcache
do
        install $T $RPM_BUILD_ROOT%{_bindir}/arm-apple-darwin10-$(basename $T)
done
ln -sf arm-apple-darwin10-libtool $RPM_BUILD_ROOT%{_bindir}/arm-apple-darwin10-ranlib

for A in $(ls as/libexec/gcc/darwin)
do
        install -d $RPM_BUILD_ROOT%{_libexecdir}/gcc/darwin/$A
        install as/libexec/gcc/darwin/$A/as \
                $RPM_BUILD_ROOT%{_libexecdir}/gcc/darwin/$A

        install -d $RPM_BUILD_ROOT%{_libexecdir}/gcc/$A-apple-darwin10
        install as/libexec/gcc/darwin/$A/as \
                $RPM_BUILD_ROOT%{_libexecdir}/gcc/$A-apple-darwin10
done

install -d $RPM_BUILD_ROOT%{_mandir}/man1
for M in man/*.1
do
        install -p -m644 $M $RPM_BUILD_ROOT%{_mandir}/man1/arm-apple-darwin10-$(basename $M)
done


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libexecdir}/*
%{_mandir}/man1/*
%doc APPLE_LICENSE


%changelog
