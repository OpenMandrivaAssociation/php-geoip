%define modname geoip
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A10_%{modname}.ini

%define mod_src "geoip.c"
%define mod_lib "-lGeoIP"
%define mod_def "-DCOMPILE_DL_GEOIP"

Summary:	Map IP address to geographic places
Name:		php-%{modname}
Version:	1.0.8
Release:	%mkrel 2
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/%{modname}/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	GeoIP-devel >= 1.4.0
Requires:	geoip >= 1.4.0
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This PHP extension allows you to find the location of an IP address - City,
State, Country, Longitude, Latitude, and other information as all, such as ISP
and connection type. For more info, please visit Maxmind's website.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

#%{_usrsrc}/php-devel/buildext %{modname} %{mod_src} %{mod_lib} %{mod_def}

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc ChangeLog README package*.xml tests
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.8-2mdv2012.0
+ Revision: 795441
- rebuild for php-5.4.x

* Tue Apr 10 2012 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.8-1
+ Revision: 790149
- 1.0.8

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.7-15
+ Revision: 761232
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.7-14
+ Revision: 696424
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.7-13
+ Revision: 695398
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.7-12
+ Revision: 646639
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.7-11mdv2011.0
+ Revision: 629798
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.7-10mdv2011.0
+ Revision: 628104
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.7-9mdv2011.0
+ Revision: 600489
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.7-8mdv2011.0
+ Revision: 588804
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.7-7mdv2010.1
+ Revision: 514548
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.7-6mdv2010.1
+ Revision: 485362
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.7-5mdv2010.1
+ Revision: 468168
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.7-4mdv2010.0
+ Revision: 451273
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1:1.0.7-3mdv2010.0
+ Revision: 397362
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.7-2mdv2010.0
+ Revision: 376993
- rebuilt for php-5.3.0RC2

* Wed Mar 11 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.7-1mdv2009.1
+ Revision: 353955
- 1.0.7

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.6-3mdv2009.1
+ Revision: 346430
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.6-2mdv2009.1
+ Revision: 341743
- rebuilt against php-5.2.9RC2

* Thu Jan 22 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.6-1mdv2009.1
+ Revision: 332497
- 1.0.6

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.5-2mdv2009.1
+ Revision: 321733
- rebuild

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.5-1mdv2009.1
+ Revision: 321646
- 1.0.5

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-3mdv2009.1
+ Revision: 310269
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-2mdv2009.0
+ Revision: 238396
- rebuild

* Fri Jun 13 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.3-1mdv2009.0
+ Revision: 218738
- 1.0.3

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.2-3mdv2009.0
+ Revision: 200203
- rebuilt for php-5.2.6

* Tue Feb 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.2-2mdv2008.1
+ Revision: 162765
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Nov 20 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.2-1mdv2008.1
+ Revision: 110768
- 1.0.2

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.1-3mdv2008.1
+ Revision: 107635
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.1-2mdv2008.0
+ Revision: 77544
- rebuilt against php-5.2.4

* Fri Aug 24 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.1-1mdv2008.0
+ Revision: 70851
- 1.0.1

* Wed Aug 15 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.0.0-1mdv2008.0
+ Revision: 63727
- 1.0.0

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.0-8mdv2008.0
+ Revision: 39496
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.0-7mdv2008.0
+ Revision: 33807
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.0-6mdv2008.0
+ Revision: 21329
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-5mdv2007.0
+ Revision: 117584
- rebuilt against new upstream version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.0-4mdv2007.1
+ Revision: 78175
- fix deps
- rebuilt for php-5.2.0
- Import php-geoip

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.0-2
- rebuilt for php-5.1.6

* Thu Aug 24 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.2.0-1mdv2007.0
- 0.2.0

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-5mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 0.1-4mdk
- rebuilt for php-5.1.3

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-3mdk
- rebuilt against php-5.1.2

* Wed Nov 30 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-2mdk
- rebuilt against php-5.1.1

* Sat Nov 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-1mdk
- rebuilt against php-5.1.0
- fix versioning

* Mon Oct 03 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_0.1-0.RC1.1mdk
- rebuilt against php-5.1.0RC1

* Wed Sep 28 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_0.1-1mdk
- initial Mandriva package

