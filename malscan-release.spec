Summary: Repository package for malscan
Name: malscan-release
Version: 1.1.5
Release: el
URL:     https://www.malscan.org
License: MIT
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
mkdir -p ${RPM_BUILD_ROOT}/etc/pki/rpm-gpg/
install -m 644 malscan.repo ${RPM_BUILD_ROOT}/etc/yum.repos.d/
install -m 644 RPM-GPG-KEY-Malscan ${RPM_BUILD_ROOT}/etc/pki/rpm-gpg/
install -m 644 RPM-GPG-KEY-Malscan-old ${RPM_BUILD_ROOT}/etc/pki/rpm-gpg/
rpm --import {%RPM_BUILD_ROOT}/etc/pki/rpm-gpg/RPM-GPG-KEY-Malscan
rpm --import {%RPM_BUILD_ROOT}/etc/pki/rpm-gpg/RPM-GPG-KEY-Malscan-old

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%attr(644,root,root) /etc/yum.repos.d/malscan.repo
%attr(644,root,root) /etc/pki/rpm-gpg/RPM-GPG-KEY-Malscan
%attr(644,root,root) /etc/pki/rpm-gpg/RPM-GPG-KEY-Malscan-old

%changelog
* Thu Oct 06 2016 Josh Grancell <josh@joshgrancell.com> 1.1.4-el
- Added GPG import.

* Thu Oct 06 2016 Josh Grancell <josh@joshgrancell.com> 1.1.4-el
- Fixed empty GPG key.

* Thu Oct 06 2016 Josh Grancell <josh@joshgrancell.com> 1.1.3-el
- Added secondary signing key for older package compatibility.

* Thu Oct 06 2016 Josh Grancell <josh@joshgrancell.com> 1.1.2-el
- Fixed a bug where the GPG key wouldn't be parsed correctly

* Thu Oct 06 2016 Josh Grancell <josh@joshgrancell.com> 1.1.1-el
- Added GPG signing to release package

* Thu Oct 06 2016 Josh Grancell <josh@joshgrancell.com> 1.1.0-el
- Updated: Added GPG key to package.

* Sat Jan 09 2016 Josh Grancell <josh@joshgrancell.com> 1.0.0-el
- Initial packaging
