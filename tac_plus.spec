Name:		tac_plus
Version:	4.0.4.15
Release:	%mkrel 1
License:	BSD
Group:		System/Servers
Summary:	TACACS+ server based on Cisco engineering release
URL:		http://www.shrubbery.net/tac_plus/
Source:		ftp://ftp.shrubbery.net/pub/%{name}/tacacs+-F%{version}.tar.gz
Source1:	tac_plus.conf
Source2:	tac_plus.pamd
Source3:	tac_plus.init
Source4:	tac_plus.sysconfig
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
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
rm -Rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}/{%{_initrddir},%{_sysconfdir}/{pam.d,sysconfig}}
install -m 640 %{SOURCE1} %{buildroot}/%{_sysconfdir}/
install -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/pam.d/%{name}
install -m 755 %{SOURCE3} %{buildroot}/%{_initrddir}/%{name}
install -m 644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
mv %{buildroot}/%{_datadir}/{tacacs+,tac_plus}

%clean
rm -Rf %{buildroot}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%defattr(-,root,root)
%{_bindir}/tac_*
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_initrddir}/%{name}
%doc %{_mandir}/man5/tac_plus.conf.5.*
%doc %{_mandir}/man8/tac_plus.8.*
%doc %{_mandir}/man8/tac_pwd.8.*
%doc %{_mandir}/man3/regexp.3.*
%doc users_guide
%{_datadir}/%{name}




%changelog
* Tue Feb 22 2011 Buchan Milne <bgmilne@mandriva.org> 4.0.4.15-1mdv2011.0
+ Revision: 639391
- update to new version 4.0.4.15

* Tue Sep 08 2009 Thierry Vignaud <tv@mandriva.org> 4.0.4.14-5mdv2010.0
+ Revision: 434267
- rebuild

* Sat Aug 02 2008 Thierry Vignaud <tv@mandriva.org> 4.0.4.14-4mdv2009.0
+ Revision: 261367
- rebuild

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 4.0.4.14-3mdv2009.0
+ Revision: 254073
- rebuild

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 4.0.4.14-1mdv2008.1
+ Revision: 140904
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Sep 06 2007 Buchan Milne <bgmilne@mandriva.org> 4.0.4.14-1mdv2008.0
+ Revision: 80515
- New version 4.0.4.14


* Sat Jan 27 2007 Buchan Milne <bgmilne@mandriva.org> 4.0.4.13-1mdv2007.0
+ Revision: 114281
- Import tac_plus

* Sat Jan 27 2007 Buchan Milne <bgmilne@mandriva.org> 4.0.4.13-1mdv
- initial package

