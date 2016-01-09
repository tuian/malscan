Summary: A Linux malware scanner
Name: malscan
Version: 1.6.0
Release: 1
URL:     http://malscan.github.io
License: GPLv2+
Group: Applications/System
BuildRoot: %{_tmppath}/%{name}-root
Requires: bash
Source0: malscan-%{version}.tar.gz
BuildArch: noarch

%description
A robust and fully featured Linux malware scanner for both servers and desktops.

%prep
%setup

%build

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/etc
mkdir -p ${RPM_BUILD_ROOT}/usr/local/share/malscan
install -m 755 malscan ${RPM_BUILD_ROOT}%{_sysconfdir}/conf.malscan

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%config(noreplace) /etc/conf.malscan

%changelog
* Fri Jan 08 2016 Josh Grancell <josh@joshgrancell.com>
- Package test
