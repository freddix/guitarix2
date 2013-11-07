%define		pre	%{nil}

Summary:	Simple Linux Rock Guitar Amplifier for JACK
Name:		guitarix2
Version:	0.28.3
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/guitarix/%{name}-%{version}%{pre}.tar.bz2
# Source0-md5:	9b535512a07d5a48e67a5cec01ee6944
BuildRequires:	boost-devel
BuildRequires:	gtkmm-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	liblrdf-devel
BuildRequires:	libsndfile-devel
BuildRequires:	lv2-devel
BuildRequires:	zita-convolver-devel
BuildRequires:	zita-resampler-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	jack-audio-connection-kit
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
guitarix is a simple Linux Rock Guitar Amplifier for jack (Jack Audio
Connektion Kit) with one input and two outputs. Designed, with GTK and
faust, to get nice thrash/metal/rock guitar sounds.

%package libs
Summary:	Guitarix - shared libraries
Group:		Libraries

%description libs
Guitarix - shared libraries.

%package -n lv2-guitarix
Summary:	LV2 GxAmplifier
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n lv2-guitarix
LV2 plugins based on Guitarix amps.

%prep
%setup -qn guitarix-%{version}%{pre}

%{__sed} -i 's/-O3 -DNDEBUG/-DNDEBUG/g' wscript
%{__sed} -i 's/Categories.*/Categories=GTK;AudioVideo;Audio;Midi;/' guitarix.desktop.in
%{__sed} -i "s/'lib'/\'%{_lib}\'/" wscript

%build
./waf configure	\
	--cxxflags="%{rpmcxxflags} -Wall"	\
	--ldflags="%{rpmldflags}"		\
	--destdir=$RPM_BUILD_ROOT		\
	--ladspadir=%{_libdir}/ladspa		\
	--prefix=%{_prefix}
./waf -v build

%install
rm -rf $RPM_BUILD_ROOT
./waf install \
	--destdir=$RPM_BUILD_ROOT

%find_lang guitarix

chmod +x $RPM_BUILD_ROOT%{_libdir}/lib*

%clean
rm -rf $RPM_BUILD_ROOT

%files -f guitarix.lang
%defattr(644,root,root,755)
%doc README changelog
%attr(755,root,root) %{_bindir}/guitarix
%attr(755,root,root) %{_libdir}/ladspa/*.so
%{_datadir}/gx_head
%{_datadir}/ladspa/rdf/guitarix.rdf
%{_datadir}/ladspa/rdf/guitarix_amp.rdf
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libgxw.so.0
%attr(755,root,root) %ghost %{_libdir}/libgxwmm.so.0
%attr(755,root,root) %{_libdir}/libgxw.so.*.*
%attr(755,root,root) %{_libdir}/libgxwmm.so.*.*

%files -n lv2-guitarix
%defattr(644,root,root,755)
%dir %{_libdir}/lv2/*.lv2
%attr(755,root,root) %{_libdir}/lv2/*.lv2/*.so
%{_libdir}/lv2/*.lv2/*.ttl
%dir %{_libdir}/lv2/*.lv2/modgui
%{_libdir}/lv2/*.lv2/modgui/*.html
%{_libdir}/lv2/*.lv2/modgui/*.json

