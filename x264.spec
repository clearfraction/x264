%global api 160
%global gitdate 20200615
%global commit0 4c9b076be684832b9141f5b6c03aaf302adca0e4
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}


Name:     x264
Version:  0.%{api}
Release:  %{?gver}%{?dist}
Epoch:    1
Summary:  A free h264/avc encoder - encoder binary
License:  GPLv2
Group:    Applications/Multimedia
Url:      https://www.videolan.org/developers/x264.html
# git branches https://repo.or.cz/x264.git/refs
Source0:  https://code.videolan.org/videolan/x264/-/archive/%{commit0}/x264-%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
BuildRequires:  nasm
BuildRequires:  pkg-config
BuildRequires:  yasm
BuildRequires:  bc 
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:       %{name} = %{epoch}:%{version}-%{release}
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

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

Be aware that the x264 library is still in early development stage. The
command line tool x264 can handle only raw YUV 4:2:0 streams at the
moment so please use mencoder or another tool that supports x264 library
for all other file types.

%package libs
Summary: Library for encoding H264/AVC video streams
Group: Development/Libraries
Provides:	%{name}-libs = %{version}-%{release}
Provides:	%{name}-libs = %{epoch}:%{version}-%{release}

%description libs
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

%package dev
Summary:     Libraries and include file for the %{name} encoder
Group:       Development/Libraries
Requires:	 %{name}-libs = %{epoch}:%{version}-%{release}
Requires: 	 pkg-config
Provides:    x264-dev = %{version}-%{release}
Provides:	 x264-dev = %{epoch}:%{version}-%{release}
Obsoletes:   x264-dev < %{version}

%description dev
x264 is a free library for encoding next-generation H264/AVC video
streams. The code is written from scratch by Laurent Aimar, Loren
Merritt, Eric Petit (OS X), Min Chen (vfw/asm), Justin Clay (vfw), Mans
Rullgard, Radek Czyz, Christian Heine (asm), Alex Izvorski (asm), and
Alex Wright. It is released under the terms of the GPL license. This
package contains a static library and a header needed for the
development with libx264. This library is needed to build
mplayer/mencoder with H264 encoding support.

%prep
%setup -n x264-%{commit0}

apiversion=$( grep '#define X264_BUILD' x264.h | cut -d' ' -f3 | sed 's/./0.&/1')   
echo "You are using $apiversion of x264"

_output=`echo "$apiversion != %{version}" | bc`
if [[ $_output == "1" ]]; then
   echo "api version is not equal to %{version}"
exit 1
else
   echo "api version is equal to %{version}"
fi

%build
export http_proxy=http://127.0.0.1:9/
export https_proxy=http://127.0.0.1:9/
export no_proxy=localhost,127.0.0.1,0.0.0.0
export LANG=C.UTF-8
export GCC_IGNORE_WERROR=1
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
export CFLAGS="$CFLAGS -O3 -ffat-lto-objects -flto=4 "
export FCFLAGS="$CFLAGS -O3 -ffat-lto-objects -flto=4 "
export FFLAGS="$CFLAGS -O3 -ffat-lto-objects -flto=4 "
export CXXFLAGS="$CXXFLAGS -O3 -ffat-lto-objects -flto=4 "
%configure --enable-shared --enable-pic 
make

%install
  make -C %{_builddir}/%{name}-%{commit0} DESTDIR=%{buildroot} install-cli
%if  %{with 10bit_depth}
  install -m 755 %{_builddir}/%{name}-10bit/x264 %{buildroot}/%{_bindir}/x264-10bit
%endif

install -dm 755 %{buildroot}/%{_libdir}
make -C %{_builddir}/%{name}-%{commit0} DESTDIR=%{buildroot} install-lib-shared %{?_smp_mflags}
%if  %{with 10bit_depth}
  make -C %{_builddir}/%{name}-10bit DESTDIR=%{buildroot} install-lib-shared %{?_smp_mflags}
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/x264


%files libs
%{_libdir}/libx264.so.%{api}


%files dev
%defattr(0644,root,root)
%{_includedir}/x264.h
%{_includedir}/x264_config.h
%{_libdir}/pkgconfig/x264.pc
%{_libdir}/libx264.so
%if %{with 10bit_depth}
%{_includedir}/x264-10bit/x264.h
%{_includedir}/x264-10bit/x264_config.h
%{_libdir}/x264-10bit/libx264.so
%{_libdir}/x264-10bit/pkgconfig/x264.pc
%endif

%changelog
# based on https://github.com/UnitedRPMs/x264
