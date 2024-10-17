Name:		tac_plus
Version:	4.0.4.15
Release:	5
License:	BSD
Group:		System/Servers
Summary:	TACACS++ server based on Cisco engineering release
URL:		https://www.shrubbery.net/tac_plus/
Source:		ftp://ftp.shrubbery.net/pub/%{name}/tacacs+-F%{version}.tar.gz
Source1:	tac_plus.conf
Source2:	tac_plus.pamd
Source3:	tac_plus.service
Source4:	tac_plus.sysconfig
Source5:        tac_plus-wrapper.sh
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
BuildRequires:	tcp_wrappers-devel pam-devel

%description
The base source for this TACACS+ package is Cisco's publicly available TACACS+
"developer's kit", for which we are grateful.

We needed a way to limit certain groups within the company from logging into
or getting enable access on certain devices. Access lists (ACLs) of a sort have
been added that match against the address of the device speaking with the
daemon.

Being paranoid, we also wanted to limit which hosts could connect to the
daemon. This can be done with tcp_wrappers via inetd, but this does not work if
the daemon is running standalone. So, calls to libwrap, the tcp_wrappers
library, have been added. For the source and more information about
tcp_wrappers, see Wietse Venema's site at http://www.porcupine.org/.

Along the way we have also added autoconf, expanded the manual pages,
cleaned-up various formatting and STD C nits, added PAM authentication support,
and fixed a few LP64 problems.

Of course we have also received some enchancement requests from users. One of
which was the addition of a host clause (per-host configuration). This has been
added; ported from Devrim Seral's implementation. See the documentation for
further information. 


%prep
%setup -q -n tacacs+-F%{version}

%build
%configure
%make

%install
%makeinstall_std

mkdir -p %{buildroot}/{%{_unitdir},%{_sysconfdir}/{pam.d,sysconfig}}
install -m 640 %{SOURCE1} %{buildroot}%{_sysconfdir}/
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -m0644 -D %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -m0755 -D %{SOURCE5} %{buildroot}%{_bindir}/tac_plus-wrapper.sh
mv %{buildroot}/%{_datadir}/{tacacs+,tac_plus}

sed "s:libexecdir:%{_libexecdir}:" -i %{buildroot}%{_unitdir}/%{name}.service
sed "s:sysconfig:%{_sysconfdir}/sysconfig:" -i %{buildroot}%{_unitdir}/%{name}.service

%clean
rm -Rf %{buildroot}

%post
%systemd_post %{name}

%preun
%systemd_preun %{name}

%files
%{_bindir}/tac_*
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0644,root,root) %{_unitdir}/%{name}.service
%doc %{_mandir}/man5/tac_plus.conf.5.*
%doc %{_mandir}/man8/tac_plus.8.*
%doc %{_mandir}/man8/tac_pwd.8.*
%doc %{_mandir}/man3/regexp.3.*
%doc users_guide
%{_datadir}/%{name}
