Name:           minmon
Version:        0.12.0
Release:        1%{?dist}
Summary:        An opinionated minimal monitoring and alarming tool

License:        MIT OR Apache-2.0
URL:            https://github.com/antedebaas/minmon
Source0:        https://github.com/antedebaas/minmon/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  rust >= 1.70
BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  openssl-devel
BuildRequires:  systemd-devel
BuildRequires:  pkgconfig
BuildRequires:  lm_sensors-devel

Requires:       glibc
Requires:       openssl
Requires:       systemd
Requires:       lm_sensors

# Disable debuginfo package generation for Rust binaries
%global debug_package %{nil}

%description
MinMon is an opinionated minimal monitoring and alarming tool for Linux.
This tool is just a single binary and a config file. No database, no GUI,
no graphs. Just monitoring and alarms. Features include filesystem usage
monitoring, memory usage tracking, network throughput monitoring, systemd
unit status checking, temperature monitoring, and various notification
methods including email, webhooks, and process execution.

%prep
%autosetup -n %{name}-%{version}

%build
# Build with full features including systemd, docker, sensors, http, and smtp support
cd %{_builddir}/%{name}-%{version} && cargo build --release --verbose --features full

%install
# Install binary
install -D -m 755 %{_builddir}/%{name}-%{version}/target/release/%{name} %{buildroot}%{_bindir}/%{name}

# Install systemd service file
install -D -m 644 %{_builddir}/%{name}-%{version}/systemd.%{name}.service %{buildroot}%{_unitdir}/%{name}.service

# Install documentation
install -d %{buildroot}%{_docdir}/%{name}
install -m 644 %{_builddir}/%{name}-%{version}/README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{name}-%{version}/CONTRIBUTING.md %{buildroot}%{_docdir}/%{name}/

# Install license files
install -m 644 %{_builddir}/%{name}-%{version}/LICENSE-MIT %{buildroot}%{_docdir}/%{name}/
install -m 644 %{_builddir}/%{name}-%{version}/LICENSE-APACHE %{buildroot}%{_docdir}/%{name}/

# Create config directory
install -d %{buildroot}%{_sysconfdir}/%{name}
# Install example config file
install -m 644 %{_builddir}/%{name}-%{version}/examples/example-config.toml %{buildroot}%{_sysconfdir}/%{name}/minmon.toml

%files
%license %{_docdir}/%{name}/LICENSE-MIT
%license %{_docdir}/%{name}/LICENSE-APACHE
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/CONTRIBUTING.md
%config(noreplace) %{_sysconfdir}/%{name}/minmon.toml
%{_bindir}/%{name}
%{_unitdir}/%{name}.service

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
* Tue Jul 16 2024 Florian Wickert <FlorianWickert@gmail.com> - 0.11.1-1
- Fixed bad cycles counter reset bug

* Tue Jul 02 2024 Florian Wickert <FlorianWickert@gmail.com> - 0.11.0-1
- Added ProcessOutputInteger and ProcessOutputMatch checks

* Wed Apr 03 2024 Florian Wickert <FlorianWickert@gmail.com> - 0.10.0-1
- Now builds with statically linked binaries
- Removed sensors support due to static linking

* Thu May 10 2024 Florian Wickert <FlorianWickert@gmail.com> - 0.9.0-1
- Added environment variable placeholder support
- Fixed filter configuration mapping

* Mon Feb 12 2024 Florian Wickert <FlorianWickert@gmail.com> - 0.7.0-1
- Added boot_delay and start_delay configuration options
- Added cron-like report scheduling

* Thu Oct 05 2023 Florian Wickert <FlorianWickert@gmail.com> - 0.6.0-1
- Added filters feature (Average, Peak, Sum)
- New stdout/stderr placeholders for ProcessExitStatus

* Thu Aug 03 2023 Florian Wickert <FlorianWickert@gmail.com> - 0.5.8-1
- Fixed state machine stability issues
- Adapted systemd service file permissions

* Wed Mar 08 2023 Florian Wickert <FlorianWickert@gmail.com> - 0.5.1-1
- Added NetworkThroughput and DockerContainerStatus checks
- Added optional http and smtp features

* Fri Apr 14 2023 Florian Wickert <FlorianWickert@gmail.com> - 0.5.3-1
- Changed to dual MIT/Apache-2.0 licensing

* Wed Jan 11 2023 Florian Wickert <FlorianWickert@gmail.com> - 0.4.0-1
- Added Temperature and SystemdUnitStatus checks
- Added configurable check timeouts

* Mon Dec 26 2022 Florian Wickert <FlorianWickert@gmail.com> - 0.3.1-1
- Added PressureAverage and ProcessExitStatus checks

* Sun Dec 18 2022 Florian Wickert <FlorianWickert@gmail.com> - 0.2.0-1
- Initial package
