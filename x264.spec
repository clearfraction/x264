%global api 164
%global gitdate 20241022
%global commit0 da14df5535fd46776fb1c9da3130973295c87aca
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:     x264
Version:  %{commit0}
Release:  %{gitdate}
Summary:  A free h264/avc encoder - encoder binary
License:  GPLv2
Group:    Applications/Multimedia
Url:      https://www.videolan.org/developers/x264.html
Source0:  https://code.videolan.org/videolan/x264/-/archive/%{commit0}/x264-%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
BuildRequires:  nasm
BuildRequires:  pkg-config
BuildRequires:  yasm
BuildRequires:  bc 
Provides:       %{name} = %{version}-%{release}
Requires:	    %{name}-libs = %{version}-%{release}

%description
x264 is a free library for encoding next-generation H264/AVC video
streams. The code is written from scratch by Laurent Aimar, Loren
Merritt, Eric Petit (OS X), Min Chen (vfw/asm), Justin Clay (vfw), Mans
Rullgard, Radek Czyz, Christian Heine (asm), Alex Izvorski (asm), and
Alex Wright. It is released under the terms of the GPL license. This
package contains a shared library and a commandline tool for encoding
H264 streams. This library is needed for mplayer/mencoder for H264
encoding support.

%package libs
Summary: Library for encoding H264/AVC video streams
Group: Development/Libraries
Provides:	%{name}-libs = %{version}-%{release}
Provides:	%{name}-libs = %{version}-%{release}

%description libs
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

%package dev
Summary:     Libraries and include file for the %{name} encoder
Group:       Development/Libraries
Requires:	 %{name}-libs = %{version}-%{release}
Requires: 	 pkg-config
Provides:    x264-dev = %{version}-%{release}
Provides:	 x264-dev = %{version}-%{release}
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
%setup -q -n %{name}-%{commit0}


%build
export LANG=C.UTF-8
export GCC_IGNORE_WERROR=1
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
export CFLAGS="$CFLAGS -O3 -Ofast -falign-functions=32 -ffat-lto-objects -flto=auto -fno-semantic-interposition -mprefer-vector-width=256 "
export FCFLAGS="$FFLAGS -O3 -Ofast -falign-functions=32 -ffat-lto-objects -flto=auto -fno-semantic-interposition -mprefer-vector-width=256 "
export FFLAGS="$FFLAGS -O3 -Ofast -falign-functions=32 -ffat-lto-objects -flto=auto -fno-semantic-interposition -mprefer-vector-width=256 "
export CXXFLAGS="$CXXFLAGS -O3 -Ofast -falign-functions=32 -ffat-lto-objects -flto=auto -fno-semantic-interposition -mprefer-vector-width=256 "
%configure --enable-shared --enable-asm --bit-depth=all
make %{?_smp_mflags}

%install
%make_install


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
/usr/bin/x264

%files libs
%defattr(-,root,root,-)
/usr/lib64/libx264.so.*

%files dev
%defattr(-,root,root,-)
/usr/include/x264.h
/usr/include/x264_config.h
/usr/lib64/pkgconfig/x264.pc
/usr/lib64/libx264.so

%changelog
# based on https://github.com/UnitedRPMs/x264
