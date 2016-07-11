Summary: Virus signature databases for malscan
Name: malscan-db
Version: 1.0
Release: 2
URL:     https://github.com/jgrancell/malscan
License: MIT
Group: Applications/System
BuildRoot: %{_tmppath}/%{name}-root
Source0: malscan-db-%{version}.tar.gz
BuildArch: noarch

%description
Virus signature databases used by malscan to detect malware on Linux systems

%prep
%setup

%build

%pre
getent group malscan >/dev/null || groupadd -r malscan
getent passwd malscan >/dev/null || useradd -r -g malscan -s /sbin/nologin -c "Malscan Service User" malscan
exit 0

%install
rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/var/lib/malscan

install main.cvd ${RPM_BUILD_ROOT}/var/lib/malscan/main.cvd
install bytecode.cvd ${RPM_BUILD_ROOT}/var/lib/malscan/bytecode.cvd
install daily.cvd ${RPM_BUILD_ROOT}/var/lib/malscan/daily.cvd

%clean
rm -rf ${RPM_BUILD_ROOT}

%post

%files
%defattr(-,root,root)
%dir %attr(755,malscan,malscan) /var/lib/malscan
%attr(644,malscan,malscan) /var/lib/malscan/main.cvd
%attr(644,malscan,malscan) /var/lib/malscan/daily.cvd
%attr(644,malscan,malscan) /var/lib/malscan/bytecode.cvd


%changelog
* Thu Jul 11 2016 Josh Grancell <josh@joshgrancell.com> 1.0-2
- Update: Updated virus databases

* Thu Jul 11 2016 Josh Grancell <josh@joshgrancell.com> 1.0-1
- New: Initial packaging of virus databases for new malscan installations
