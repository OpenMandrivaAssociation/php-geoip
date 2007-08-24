%define modname geoip
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A10_%{modname}.ini

%define mod_src "geoip.c"
%define mod_lib "-lGeoIP"
%define mod_def "-DCOMPILE_DL_GEOIP"

Summary:	Map IP address to geographic places
Name:		php-%{modname}
Version:	1.0.1
Release:	%mkrel 1
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/%{modname}/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	GeoIP-devel >= 1.4.0
Requires:	geoip >= 1.4.0
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc ChangeLog README package*.xml tests
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
