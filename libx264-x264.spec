#
# spec file for package libx264
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define _lto_cflags %{nil}
%define soname  155
%define svn     20190201
Name:           libx264-x264
Version:        0.%{soname}svn%{svn}
Release:        2.7
Summary:        x264 cli tool
License:        GPL-2.0+
Group:          Productivity/Multimedia/Video/Editors and Convertors
Url:            http://www.videolan.org/developers/x264.html
Source:         ftp://ftp.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-%{svn}-2245-stable.tar.bz2
Patch0:         x264-use-shared-library.patch
Patch1:         0001-cli-Fix-linking-with-system-libx264-on-x86.patch
BuildRequires:  nasm
BuildRequires:  pkg-config
BuildRequires:  yasm
BuildRequires:  pkgconfig(ffms2)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
x264 is a free library for encoding next-generation H264/AVC video
streams. The code is written from scratch by Laurent Aimar, Loren
Merritt, Eric Petit (OS X), Min Chen (vfw/asm), Justin Clay (vfw), Mans
Rullgard, Radek Czyz, Christian Heine (asm), Alex Izvorski (asm), and
Alex Wright. It is released under the terms of the GPL license. This
package contains a shared library and a commandline tool for encoding
H264 streams. This library is needed for mplayer/mencoder for H264
encoding support.

Encoder features:
- CAVLC/CABAC
- Multi-references
- Intra: all macroblock types (16x16, 8x8, and 4x4 with all predictions)
- Inter P: all partitions (from 16x16 down to 4x4)
- Inter B: partitions from 16x16 down to 8x8 (including skip/direct)
- Ratecontrol: constant quantizer, single or multipass ABR, optional VBV
- Scene cut detection
- Adaptive B-frame placement
- B-frames as references / arbitrary frame order
- 8x8 and 4x4 adaptive spatial transform
- Lossless mode
- Custom quantization matrices
- Parallel encoding of multiple slices (currently disabled)

%package %{soname}
Summary:        A free h264/avc encoder - encoder binary
Group:          System/Libraries

%description %{soname}
x264 is a free library for encoding next-generation H264/AVC video
streams. The code is written from scratch by Laurent Aimar, Loren
Merritt, Eric Petit (OS X), Min Chen (vfw/asm), Justin Clay (vfw), Mans
Rullgard, Radek Czyz, Christian Heine (asm), Alex Izvorski (asm), and
Alex Wright. It is released under the terms of the GPL license. This
package contains a static library and a header needed for the
development with libx264. This library is needed to build
mplayer/mencoder with H264 encoding support.

%package -n x264
Summary:        Binaries for x264 streams conversions

%description -n x264
x264 is a free library for encoding next-generation H264/AVC video
streams. The code is written from scratch by Laurent Aimar, Loren
Merritt, Eric Petit (OS X), Min Chen (vfw/asm), Justin Clay (vfw), Mans
Rullgard, Radek Czyz, Christian Heine (asm), Alex Izvorski (asm), and
Alex Wright. It is released under the terms of the GPL license. This
package contains a static library and a header needed for the
development with libx264. This library is needed to build
mplayer/mencoder with H264 encoding support.

%package devel
Summary:        Libraries and include file for the %{name} encoder
Group:          Development/Libraries/C and C++
Requires:       %{name}-%{soname} = %{version}
Provides:       x264-devel = %{version}
Obsoletes:      x264-devel < %{version}

%description devel
x264 is a free library for encoding next-generation H264/AVC video
streams. The code is written from scratch by Laurent Aimar, Loren
Merritt, Eric Petit (OS X), Min Chen (vfw/asm), Justin Clay (vfw), Mans
Rullgard, Radek Czyz, Christian Heine (asm), Alex Izvorski (asm), and
Alex Wright. It is released under the terms of the GPL license. This
package contains a static library and a header needed for the
development with libx264. This library is needed to build
mplayer/mencoder with H264 encoding support.

%prep
%setup -n x264-snapshot-%{svn}-2245-stable
%patch1 -p1

%build
FAKE_BUILDDATE=$(LC_ALL=C date -u -r %{_sourcedir}/%{name}.changes '+%%b %%e %%Y')
sed -i "s/__DATE__/\"$FAKE_BUILDDATE\"/" x264.c

%configure \
  --disable-lsmash \
  --disable-opencl \
  --enable-shared \
  --enable-swscale \
  --enable-lavf \
  --enable-ffms \
  --disable-gpac \
  --enable-pic
make %{?_smp_mflags}

%install
install -Dm 755 x264 %{buildroot}/%{_bindir}/x264

rm -f %{buildroot}%{_libdir}/%{name}.so
rm -f %{buildroot}%{_libdir}/%{name}.a
ln -s %{name}.so.%{soname} %{buildroot}%{_libdir}/%{name}.so
%endif

%files -n x264
%defattr(-,root,root)
%doc doc/*.txt
%attr(0755,root,root) %{_bindir}/x264

%post -n %{name}-%{soname} -p /sbin/ldconfig
%postun -n %{name}-%{soname} -p /sbin/ldconfig

%files %{soname}
%defattr(0644,root,root)
%{_libdir}/%{name}.so.%{soname}

%files devel
%defattr(0644,root,root)
%{_includedir}/x264.h
%{_includedir}/x264_config.h
%{_libdir}/pkgconfig/x264.pc
%{_libdir}/%{name}.so
%endif

%changelog
* Sat Feb  2 2019 antonio.larrosa@gmail.com
- Update to 20190201 snapshot
  * Unify 8-bit and 10-bit CLI and libraries
  - Add 'i_bitdepth' to x264_param_t with the corresponding
    '--output-depth' CLI option to set the bit depth at runtime.
  * x86inc: Fix VEX -> EVEX instruction conversion stable
  * configure: Fix required version checks for lavf and...
  * Fix float division by zero in weightp analysis
  * Fix undefined behavior of left shift for CAVLC encoding
  * Fix integer overflow in slicetype_path_cost
  * cli: Fix preset help listing
  * ppc: Fix zigzag_interleave
  * Fix clang stack alignment issues
  * Fix missing bs_flush in AUD writing
  * Fix possible undefined behavior of right shift
  * Make bs_align_10 imply bs_flush
  * Fix theoretically incorrect cost_mv_fpel free
  * configure: Fix ambiguous "$(("
  * Fix --qpmax default value in fullhelp
  * x86: Correctly use v-prefix for instructions with opmasks
  * configure: Only use gas-preprocessor with armasm for...
- Bump soname to 155 following upstream changes.
- Rebase x264-use-shared-library.patch
- Add 0001-cli-Fix-linking-with-system-libx264-on-x86.patch from
  upstream to fix building the cli x264 tool on x86.
* Thu Apr 12 2018 zaitor@opensuse.org
- Bump soname in baselibs.conf, forgotten i previous version
  update.
* Fri Mar 23 2018 enzokiel@kabelmail.de
- Build with nasm >= 2.13 for openSUSE Leap 42.3 and SLE-12.
* Tue Mar  6 2018 zaitor@opensuse.org
- Update to 20180305 snapshot.
- Bump soname to 152 following upstream changes.
- Conditionally BuildRequire nasm for current versions of
  openSUSE and pass conditional --disable-asm to openSUSE Leap 43.3
  and SLE-12.
* Thu Aug 17 2017 aloisio@gmx.com
- Update to 20170816 snapshot
* Tue Dec 20 2016 scarabeus@opensuse.org
- Update to 20161220 snapshot
- Update homepage
- Move x264 package here there is no reason for the split
* Tue Sep  6 2016 ismail@i10z.com
- Update to 20160905 snapshot
* Sun May  1 2016 aloisio@gmx.com
- Update to 20160430 snapshot
- Refreshed x264-use-shared-library.patch
* Wed Aug  5 2015 ismail@i10z.com
- update to 20150804 snapshot
* Sun Mar  1 2015 i@margueirte.su
- update version 20141218
* Wed Nov  5 2014 i@margueirte.su
- update version 20141104
* Sat Mar 22 2014 i@margueirte.su
- update version 20140321.
* Tue Nov 19 2013 obs@botter.cc
- add -fno-aggressive-loop-optimizations to extra-cflags in
  configure for >= 13.1 (specfile), see also
  https://bugs.launchpad.net/ubuntu/+source/x264/+bug/1241772
  MAY BE REMOVED on upstream fix
* Wed Jul 24 2013 i@margueirte.su
- update version 20130723.
* Thu Mar  7 2013 marguerite@opensuse.org
- fallback to 8-bit depth again.
  * A user said he still need 8-bit to use `baseline` profile
    for very old android phones.
* Sun Feb 24 2013 marguerite@opensuse.org
- update version 20130224.
- enable 10 bit depth by default.
* Thu Nov  1 2012 pascal.bleser@opensuse.org
- only build the x264 library, to avoid cycles with ffmpeg (which
  requires libx264)
* Sat Sep 29 2012 Manfred.Tremmel@iiv.de
- update to snapshot 20120928
* Sat May 26 2012 Manfred.Tremmel@iiv.de
- update to snapshot 20120525
* Sat Apr 14 2012 Manfred.Tremmel@iiv.de
- update to snapshot 20120414
* Mon Mar 12 2012 toddrme2178@gmail.com
- Cleaned up spec file formatting
- Added 32bit compatibility version (needed by
  gstreamer-0_10-plugins-ugly-orig-addon-32bit)
* Fri Jan 27 2012 Manfred.Tremmel@iiv.de
- update to snapshot 20120126
* Tue Dec 27 2011 Manfred.Tremmel@iiv.de
- update to snapshot 20111226
* Fri Sep 23 2011 Manfred.Tremmel@iiv.de
- update to snapshot 20111122
* Thu Sep  8 2011 Manfred.Tremmel@iiv.de
- update to snapshot 20110907
* Thu Jun 23 2011 Manfred.Tremmel@iiv.de
- update to snapshot 20110622
* Sat May 28 2011 Manfred.Tremmel@iiv.de
- update to snapshot 20110527
* Sat Apr 23 2011 reddwarf@opensuse.org
- remove build timestamp
- remove execution permissions from library
* Sat Feb 26 2011 Manfred.Tremmel@iiv.de
- update to snapshot 20110225
* Sun Jan 16 2011 Manfred.Tremmel@iiv.de
- update to snapshot 20110115
* Sun Oct 17 2010 Manfred.Tremmel@iiv.de
- update to snapshot 20101016
* Sun Oct  3 2010 Manfred.Tremmel@iiv.de
- update to snapshot 20101002
* Tue Jun 29 2010 ludwig.nussel@gmx.de
- require pkg-config
- link binary against shared library
* Wed Jun 16 2010 Manfred.Tremmel@iiv.de
- update to snapshot 20100615
* Tue May 18 2010 Manfred.Tremmel@iiv.de
- update to snapshot 20100517
* Mon Apr 26 2010 Manfred.Tremmel@iiv.de
- update to snapshot 20100425
  now able to create Blue Ray compatible h.264 streams
* Sat Apr  3 2010 Manfred.Tremmel@iiv.de
- update to snapshot 20100402
* Sun Feb 28 2010 Manfred.Tremmel@iiv.de
- update to snapshot 20100227
* Wed Feb 17 2010 Manfred.Tremmel@iiv.de
- update to snapshot 20100216
* Sat Feb  6 2010 Manfred.Tremmel@iiv.de
- update to snapshot 20100205
* Wed Jan 27 2010 Manfred.Tremmel@iiv.de
- rebuild because of no submit with the last build
* Sat Jan 23 2010 Manfred.Tremmel@iiv.de
- update to snapshot 20100122
* Sat Jan  2 2010 Manfred.Tremmel@iiv.de
- update to svn 20100101
* Tue Dec 15 2009 Manfred.Tremmel@iiv.de
- added a patch to fix broken ffmpeg defaults instead of aborting
* Fri Dec 11 2009 Manfred.Tremmel@iiv.de
- update to svn 20091211
* Mon Nov 23 2009 Manfred.Tremmel@iiv.de
- update to svn 20091123
* Tue Aug 25 2009 Manfred.Tremmel@iiv.de
- updated to snapshot 20090624
* Sat Jun 27 2009 Manfred.Tremmel@iiv.de
- updated to snapshot 20090627
* Sun May 10 2009 Manfred.Tremmel@iiv.de
- updated to snapshot 20090510
* Tue Mar 10 2009 Manfred.Tremmel@iiv.de
- updated to snapshot 20090310
* Sat Feb  7 2009 Manfred.Tremmel@iiv.de
- updated to snapshot 20090206
* Thu Nov  6 2008 Manfred.Tremmel@iiv.de
- updated to snapshot 20081105
* Sat Oct  4 2008 Manfred.Tremmel@iiv.de
- updated to snapshot 20081004
* Wed Sep 17 2008 Manfred.Tremmel@iiv.de
- updated to snapshot 20080917
* Thu Aug 14 2008 Manfred.Tremmel@iiv.de
- updated to snapshot 20080814
- recompile with new yasm version
* Sat Aug  9 2008 Manfred.Tremmel@iiv.de
- updated to snapshot 20080809
* Tue Jun 17 2008 Manfred.Tremmel@iiv.de
- updated to snapshot 20080617
- also included snapshot 20071225 lib for compatibility reasons
* Wed Apr 30 2008 guru@unixtech.be
- fixed file permissions, thanks to Christian Morales Vega <cmorve69@yahoo.es>
* Mon Dec 31 2007 guru@unixtech.be
- made Requires in main package require the exact version-release
- fixed License tag according to 10.3 packaging policies
- added Provides/Obsoletes for proper upgrading of x264=>libx264-devel
* Wed Dec 26 2007 leon@links2linux.de
- updated to snapshot 20071225
- changed the spec according to the new library policy, thanks Detlef
- changed the group according to SPC guidelines
* Mon Nov  6 2006 detlef@links2linux.de
- update to snapshot-20061031-2245
* Wed Nov  1 2006 leon@links2linux.de
- new release
* Wed Apr 26 2006 leon@links2linux.de
- updated to the newest tarball (to fix PPC compiling)
- match the new library revision (libx264.so.46)
* Tue Apr 18 2006 leon@links2linux.de
- updated to the newest tarball
- removed the syntax patch since it has been merged
- remove yasm from BuildRequires on x86
* Wed Mar 22 2006 henne@links2linux.de
- introduce a build section <:)
- full url for source
* Sat Mar 18 2006 leon@links2linux.de
- Initial release for packman.
