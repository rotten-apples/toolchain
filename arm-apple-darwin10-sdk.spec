# Do not let RPM modify files in our tree
%global __spec_install_post %{nil}

%global _target arm-apple-darwin10
%global _program_prefix %{_target}-

Name:           %{_program_prefix}sdk
Version:        iPhoneSDK4_3
Release:        1
Summary:        Header and symbol files for iOS development kit

Group:          Development/Libraries
License:        Proprietary
URL:            http://developer.apple.com/ios/
Source0:        %{version}.pkg
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  xar cpio
BuildArch:      noarch

%description
This package contains header and symbol files for various iOS frameworks
extracted from the official software development kit. Useful to cross-build
applications for iOS.


%prep
%setup -q -c -T
xar -xf %{SOURCE0} && zcat Payload |cpio -di


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}

cp -a Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS4.3.sdk \
        $RPM_BUILD_ROOT%{_prefix}/%{_target}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_prefix}/%{_target}
%exclude %{_prefix}/%{_target}/usr/lib/gcc


%changelog
