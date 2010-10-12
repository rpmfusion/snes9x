Summary: Super Nintendo Entertainment System emulator
Name: snes9x
Version: 1.52
Release: 1%{?dist}
License: Other
Group: Applications/Emulators
URL: http://code.google.com/p/snes9x-gtk/
Source: http://snes9x-gtk.googlecode.com/files/snes9x-%{version}-src.tar.bz2
# http://download.sessionclan.de/overfiend/snes9x/snes9x-1.52-src.fix4.diffs.zip
Patch0: snes9x-1.52-core.fix4.diff
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc-c++
BuildRequires: zlib-devel, libpng-devel
BuildRequires: libXv-devel, libXrandr-devel
BuildRequires: nasm
BuildRequires: intltool
BuildRequires: gtk2-devel, libglade2-devel
BuildRequires: SDL-devel
BuildRequires: portaudio-devel
BuildRequires: alsa-lib-devel
BuildRequires: pulseaudio-libs-devel

%description
Snes9x is a portable, freeware Super Nintendo Entertainment System (SNES)
emulator. It basically allows you to play most games designed for the SNES
and Super Famicom Nintendo game systems on your computer.


%prep
%setup -q -n %{name}-%{version}-src
%patch0 -p0 -b .fixes


%build
# Workaround for all of the missing links (as of 1.52)
export CFLAGS="%{optflags} -lX11 -ldl -lXext"
export CXXFLAGS="%{optflags} -lX11 -ldl -lXext"
# First, build the GTK version
cd gtk
%configure \
  --without-oss \
  --with-netplay
%{__make} %{?_smp_mflags}
cd ..
# Second, build the CLI version
cd unix
%configure \
  --enable-netplay
%{__make} %{?_smp_mflags}
cd ..


%install
%{__rm} -rf %{buildroot}
cd gtk
%{__make} install DESTDIR=%{buildroot}
cd ..
%find_lang snes9x-gtk
%{__install} -p -m 0755 unix/snes9x %{buildroot}%{_bindir}/snes9x


%clean
%{__rm} -rf %{buildroot}


%files -f snes9x-gtk.lang
%defattr(-,root,root,-)
%doc gtk/doc/* unix/docs/readme_unix.html
%{_bindir}/snes9x
%{_bindir}/snes9x-gtk
%{_datadir}/applications/snes9x.desktop
%{_datadir}/icons/hicolor/*/apps/snes9x.*


%changelog
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

