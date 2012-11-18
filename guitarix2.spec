%define		pre	%{nil}

Summary:	Simple Linux Rock Guitar Amplifier for JACK
Name:		guitarix2
Version:	0.24.3
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/guitarix/%{name}-%{version}%{pre}.tar.bz2
# Source0-md5:	29cbb9676ddc12cb2653bbef5164441c
BuildRequires:	boost-devel
BuildRequires:	gtkmm-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	liblrdf-devel
BuildRequires:	libsndfile-devel
BuildRequires:	zita-convolver-devel
BuildRequires:	zita-resampler-devel
Requires:	jack-audio-connection-kit
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
guitarix is a simple Linux Rock Guitar Amplifier for jack (Jack Audio
Connektion Kit) with one input and two outputs. Designed, with GTK and
faust, to get nice thrash/metal/rock guitar sounds.

%prep
%setup -qn guitarix-%{version}%{pre}

sed -i -e 's/-O3 -DNDEBUG/-DNDEBUG/g' wscript

sed -i 's/Categories.*/Categories=GTK;AudioVideo;Audio;Midi;/' guitarix.desktop.in

%build
./waf configure		\
	--cxxflags="%{rpmcxxflags} -Wall -std=c++0x"	\
	--destdir=$RPM_BUILD_ROOT			\
	--ladspadir=%{_libdir}/ladspa			\
	--prefix=%{_prefix}
./waf -v build

%install
rm -rf $RPM_BUILD_ROOT
./waf install \
	--destdir=$RPM_BUILD_ROOT

%find_lang guitarix

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

