Name:           ld64
Version:        97.17
Release:        1%{?dist}
Summary:        Linker for Mach-O files

Group:          Development/Tools
License:        APSL
URL:            http://www.opensource.apple.com/release/ios-433/

Source0:        http://www.opensource.apple.com/tarballs/%{name}/%{name}-%{version}.tar.gz
Patch1:         0001-Snapshot-local-changes-to-ld64.patch
Patch2:         0002-Add-more-missing-headers-to-ld64.patch
Patch3:         0003-Add-missing-headers.patch
Patch4:         0004-Drop-OpenBSDism.patch
Patch5:         0005-Comment-out-more-of-LTO-support.patch
Patch6:         0006-Get-rid-of-_NSGetExecutablePath-use.patch
Patch7:         0007-Publicize-fWriters.patch
Patch8:         0008-Restore-support-for-aspen_version_min.patch
Patch666: ld64-f16.patch

Source1:        http://www.opensource.apple.com/tarballs/libunwind/libunwind-30.tar.gz
Patch11:        0001-Fix-i386-register-names.patch
Patch12:        0002-Make-it-build.patch
Patch13:        0003-Fix-abort.patch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  xnu-headers
BuildRequires:  openssl-devel

%description
Static linker for Mach-O object files, typically used in NeXT and Darwin 
operating systems.


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
%patch666 -p1

ln -sf ../../libunwind-30/src src/ld/libunwind
tar xzf %{SOURCE1}
cd libunwind-30
%patch11 -p1
%patch12 -p1
%patch13 -p1
cd ..


%build
make %{?_smp_mflags} -f Makefile.linux CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"


%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
install src/ld/ld64 $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -pm644 doc/man/man1/ld.1 $RPM_BUILD_ROOT%{_mandir}/man1/ld64.1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*
%doc APPLE_LICENSE


%changelog
