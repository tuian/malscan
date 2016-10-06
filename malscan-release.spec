Summary: Repository package for malscan
Name: malscan-release
Version: 1.1.0
Release: 1
URL:     http://malscan.github.io
License: GPLv2+
Group: Applications/System
BuildRoot: %{_tmppath}/%{name}-root
Requires: bash
Requires: epel-release
Source0: malscan-release-%{version}.tar.gz
BuildArch: x86_64

%description
Repository installer package for malscan, a linux malware scanner

%prep
%setup

%build

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/etc/yum.repos.d/
install -m 644 malscan.repo ${RPM_BUILD_ROOT}/etc/yum.repos.d/
install -m 644 RPM-GPG-KEY-Malscan ${RPM_BUILD_ROOT}/etc/pki/rpm-gpg/

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)

%changelog
* Thu Oct 06 2016 Josh Grancell <josh@joshgrancell.com>
- Updated: Added GPG key to package.
* Sat Jan 09 2016 Josh Grancell <josh@joshgrancell.com>
- Initial packaging
