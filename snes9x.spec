Summary: Super Nintendo Entertainment System emulator
Name: snes9x
Version: 1.58
Release: 1%{?dist}
License: Other
URL: http://www.snes9x.com/
Source0: https://github.com/snes9xgit/snes9x/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: %{name}.appdata.xml
# Fix CFLAGS usage in CLI version
Patch0: %{name}-1.56.1-unix_flags.patch
BuildRequires: gcc-c++
BuildRequires: autoconf
BuildRequires: zlib-devel
BuildRequires: libpng-devel
BuildRequires: libXv-devel
BuildRequires: libXrandr-devel
BuildRequires: libGL-devel
BuildRequires: nasm
BuildRequires: intltool
BuildRequires: gtk3-devel
BuildRequires: libglade2-devel
BuildRequires: SDL2-devel
BuildRequires: libxml2-devel
%if 0%{?fedora} >= 30
BuildRequires:	minizip-compat-devel
%else
BuildRequires:	minizip-devel
%endif
BuildRequires: portaudio-devel
BuildRequires: alsa-lib-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
Requires:      hicolor-icon-theme

%description
Snes9x is a portable, freeware Super Nintendo Entertainment System (SNES)
emulator. It basically allows you to play most games designed for the SNES
and Super Famicom Nintendo game systems on your computer.

%package gtk
Summary: Super Nintendo Entertainment System emulator - GTK version
Requires: hicolor-icon-theme

%description gtk
Snes9x is a portable, freeware Super Nintendo Entertainment System (SNES)
emulator. It basically allows you to play most games designed for the SNES
and Super Famicom Nintendo game systems on your computer.

This package contains a graphical user interface using GTK+.


%prep
%setup -q
%patch0 -p1

# Remove bundled libs
rm -rf unzip


%build
# Build GTK version
pushd gtk
./autogen.sh
%configure \
    --disable-silent-rules \
    --without-oss
%make_build
popd

# Build CLI version
pushd unix
autoreconf
%configure \
    --with-system-zip \
    --enable-netplay
%make_build
popd


%install
# Install GTK version
%make_install -C gtk

# Install CLI version
mkdir -p %{buildroot}%{_bindir}
install -p -m 0755 unix/snes9x %{buildroot}%{_bindir}

# Validate desktop file
desktop-file-validate \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install AppData file
install -d %{buildroot}%{_datadir}/metainfo
install -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/metainfo
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.appdata.xml

%find_lang snes9x-gtk


%files
%license LICENSE
%doc docs/changes.txt
%doc unix/docs/readme_unix.html
%{_bindir}/snes9x


%files gtk -f snes9x-gtk.lang
%license LICENSE
%doc docs/changes.txt
%doc gtk/AUTHORS
%{_bindir}/snes9x-gtk
%{_datadir}/%{name}
%{_datadir}/metainfo/snes9x.appdata.xml
%{_datadir}/applications/snes9x.desktop
%{_datadir}/icons/hicolor/*/apps/snes9x.*


%changelog
* Fri Dec 21 2018 Andrea Musuruane <musuruan@gmail.com> - 1.58-1
- Updated to 1.58

* Sun Nov 25 2018 Andrea Musuruane <musuruan@gmail.com> - 1.57-1
- Updated to 1.57
- Updated BR to minizip-compat-devel for F30+

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.56.2-3
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 1.56.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 23 2018 Andrea Musuruane <musuruan@gmail.com> - 1.56.2-1
- Updated to 1.56.2

* Thu Jun 21 2018 Andrea Musuruane <musuruan@gmail.com> - 1.56.1-3
- Fixed joystick support (BZ #4947)

* Sat Jun 16 2018 Andrea Musuruane <musuruan@gmail.com> - 1.56.1-2
- Added an upstream patch to fix compiling on ppc64

* Sat Jun 16 2018 Andrea Musuruane <musuruan@gmail.com> - 1.56.1-1
- Updated to 1.56.1
- Removed obsolete scriptlets

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Nov 26 2017 Andrea Musuruane <musuruan@gmail.com> - 1.55-1
- Updated to 1.55
- Added AppData file
- Added missing Requires

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.54.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.54.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Andrea Musuruane <musuruan@gmail.com> - 1.54.1-1
- Updated to 1.54.1
- Made separate gtk package
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Dropped cleaning at the beginning of %%install

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 1.53-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Mar 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.53-4
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Mar 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.53-3
- Rebuilt for c++ ABI breakage

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun  1 2011 Matthias Saou <http://freshrpms.net/> 1.53-1
- Update to 1.53.
- Remove no longer needed patch and compile time lib hacks.

* Thu Oct 14 2010 Matthias Saou <http://freshrpms.net/> 1.52-2
- Add missing scriplets now that there are icons and a MimeType.

* Wed Aug 11 2010 Matthias Saou <http://freshrpms.net/> 1.52-1
- Update to 1.52, which is now hosted at google (sort of a unique fork).
- Now include the new gtk version, it also supports OpenGL.

* Wed May  6 2009 Matthias Saou <http://freshrpms.net/> 1.51-4
- Include patch to fix the current compilation errors.
- Quiet setup.

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.51-3
- rebuild for new F11 features

* Sat Oct 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.51-2
- rebuild for RPM Fusion
- always build for xorg

* Sat Aug 11 2007 Matthias Saou <http://freshrpms.net/> 1.51-1
- Update to 1.51.
- Bundle a second binary, osnes9x, the OpenGL version.
- Include useful readme_unix.txt.
- Remove no longer needed externc patch.

* Tue Oct 17 2006 Matthias Saou <http://freshrpms.net/> 1.50-1
- Update to 1.5... well, luckily it's also called 1.50 in some places, ugh.
- Update source URL.
- Include patch to fix C++ and C extern declarations.
- Remove no longer needed gcc4 patch.
- Remove no longer needed autoreconf and its build requirements.
- Remove no longer needed usagemsg patch, all now fits fine in 80 columns.
- Remove --without-assembler since build works again on i386 with it.
- Note : --with opengl doesn't work... some error in unix/opengl.cpp.

* Wed Mar 22 2006 Matthias Saou <http://freshrpms.net/> 1.43-7
- Add missing modular X build requirement.
- Add autoreconf call to fix configure's X detection.

* Fri Mar 17 2006 Matthias Saou <http://freshrpms.net/> 1.43-6
- Release bump to drop the disttag number in FC5 build.

* Tue Jan 24 2006 Matthias Saou <http://freshrpms.net/> 1.43-5
- Add wmclass patch from Bryan Moffit.

* Fri Jan 13 2006 Matthias Saou <http://freshrpms.net/> 1.43-4
- Add modular xorg build conditional.

* Thu Nov 10 2005 Matthias Saou <http://freshrpms.net/> 1.43-3
- Merge things from Ville's package : Usage message patch, optional OpenGL
  support using --with opengl.

* Thu May  5 2005 Matthias Saou <http://freshrpms.net/> 1.43-2
- Include gcc4 patch from Debian.
- Pass --without-assembler since build fails on i386/getset.S otherwise.

* Sun Apr 17 2005 Matthias Saou <http://freshrpms.net/> 1.43-1
- Update to 1.43 final (was WIP1).

* Sat Dec 18 2004 Matthias Saou <http://freshrpms.net/> 1.43-0
- Initial RPM release.

