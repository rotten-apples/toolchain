Name:           xnu-headers
# http://www.opensource.apple.com/release/mac-os-x-1071/
Version:        1228.5.90
Release:        0.3.MacOSX10.6
Summary:        Header files from XNU kernel

Group:          Development/Libraries
License:        APSL and BSD
URL:            http://www.opensource.apple.com/release/mac-os-x-1071/
Source0:        MacOSX10.6.pkg
Source1:        http://www.opensource.apple.com/tarballs/cctools/cctools-795.tar.gz
Patch0:         0001-Remove-__unused.patch
Patch1:         0002-Fix-up-libc.h.patch
Patch2:         0003-toolwhip-changes.patch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  xar cpio
BuildArch:      noarch

BuildRequires:  xar cpio
BuildArch:      noarch

%description


%prep
%setup -q -c -T
set -o pipefail
xar -xf %{SOURCE0} && zcat Payload |cpio -di
tar -xzf %{SOURCE1}
%patch0 -p1
%patch1 -p1
%patch2 -p1


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_includedir}/xnu{,/sys}
cp -al SDKs/MacOSX10.6.sdk/usr/include/{i386,architecture,mach{,-o,_debug,ine},libkern,libc.h,Availability*.h,libunwind.h} \
        $RPM_BUILD_ROOT%{_includedir}/xnu
ln -f SDKs/MacOSX10.6.sdk/usr/include/sys/_types.h \
        $RPM_BUILD_ROOT%{_includedir}/xnu/sys/_types.h
ln -f cctools-795/include/mach-o/dyld_priv.h \
        $RPM_BUILD_ROOT%{_includedir}/xnu/mach-o/
cp -al cctools-795/include/mach-o/arm \
        $RPM_BUILD_ROOT%{_includedir}/xnu/mach-o/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_includedir}/xnu


%changelog
