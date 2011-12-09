%define major 0
%define libname %mklibname %{name} %major
%define develname %mklibname -d %{name}
%define gioname gio2.0

%define enable_gphoto2 1
%define enable_iphone 1

Summary: Glib VFS library
Name: gvfs
Version: 1.10.1
Release: 1
License: LGPLv2+
Group: System/Libraries
Url: http://www.gnome.org/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz
Source1: bash-completion
#gw from Ubuntu, fix music player detection
# https://bugs.freedesktop.org/show_bug.cgi?id=24500
Patch0: gvfs-music-player-mimetype.patch
Patch1: gvfs-1.6.7_glibh.patch

BuildRequires:	intltool
BuildRequires:	cdda-devel
BuildRequires:	expat-devel
BuildRequires:	pkgconfig(glib-2.0) >= 2.31.0
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gmodule-no-export-2.0)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(avahi-glib)
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	pkgconfig(smbclient)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(openobex)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(gdu)
BuildRequires:	pkgconfig(libbluray)
BuildRequires:	pkgconfig(libsoup-gnome-2.4) >= 2.26.0
BuildRequires:	pkgconfig(libcdio_paranoia)
BuildRequires:	pkgconfig(gudev-1.0)
%if %{enable_gphoto2}
BuildRequires:	pkgconfig(libgphoto2)
%endif
%if %{enable_iphone}
BuildRequires:	pkgconfig(libimobiledevice-1.0) >= 1.1.0
BuildRequires:	pkgconfig(libplist) >= 0.15
%endif

Requires(post): %{gioname} >= 2.23.4-2
Requires(postun): %{gioname} >= 2.23.4-2
Suggests: %{name}-fuse
Suggests: %{name}-smb
Suggests: %{name}-archive
#Suggests: %{name}-obexftp
%if %{enable_gphoto2}
Suggests: %{name}-gphoto2
%endif
Conflicts: %{libname} < 1.6.7-4

%description
This is a Virtual File System library based on gio and Glib.

%package -n %{libname}
Group: System/Libraries
Summary: Glib VFS library

%description -n %{libname}
This is a Virtual File System library based on gio and Glib.

%package -n %{develname}
Group: Development/C
Summary: Glib VFS Library - development files
Requires: %{libname} = %{version}-%{release}
Provides: libgvfs-devel = %{version}-%{release}

%description -n %{develname}
This is a Virtual File System library based on gio and Glib.

%package fuse
Summary: FUSE support for gvfs
Group: System/Libraries
Requires: %{name} = %{version}-%{release}
Requires: fuse

%description fuse
This package provides support for applications not using gio
to access the gvfs filesystems.

%package smb
Summary: Windows fileshare support for gvfs
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description smb
This package provides support for reading and writing files on windows
shares (SMB) to applications using gvfs.

%package archive
Summary: Archiving support for gvfs
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description archive
This package provides support for accessing files inside Zip and Tar archives,
as well as ISO images, to applications using gvfs.

%package obexftp
Summary: ObexFTP support for gvfs
Group: System/Libraries
Requires: %{name} = %{version}-%{release}
Requires: obex-data-server >= 0.3.4-6

%description obexftp
This package provides support for reading files on Bluetooth mobile phones
and devices through ObexFTP to applications using gvfs.

%package gphoto2
Summary: gphoto2 support for gvfs
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description gphoto2
This package provides support for reading and writing files on
PTP based cameras (Picture Transfer Protocol) and MTP based
media players (Media Transfer Protocol) to applications using gvfs.

%package iphone
Summary: iphone support for gvfs
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description iphone
This package provides support for reading and writing files on
the iPhone and the iPod TouchP to applications using gvfs.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--with-dbus-service-dir=%{_datadir}/dbus-1/services \
%if %{enable_gphoto2}
	--enable-gphoto2
%else
	--disable-gphoto2
%endif

%make

%install
rm -rf %{buildroot}
%makeinstall_std
find %{buildroot}%{_libdir} -name '*.la' -type f -delete -print
%find_lang gvfs

# upstream bash completion is installed in the wrong place, with the wrong perms
# and redefine system variables without notice
rm -f %{buildroot}%{_sysconfdir}/profile.d/gvfs-bash-completion.sh
install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}

%files -f gvfs.lang
%{_sysconfdir}/bash_completion.d/gvfs
%{_bindir}/gvfs-*
%{_libdir}/gio/modules/libgioremote-volume-monitor.so
%{_libdir}/gio/modules/libgvfsdbus.so
%{_libexecdir}/gvfs-gdu-volume-monitor
%{_libexecdir}/gvfsd
%{_libexecdir}/gvfsd-afp
%{_libexecdir}/gvfsd-afp-browse
%{_libexecdir}/gvfsd-burn
%{_libexecdir}/gvfsd-cdda
%{_libexecdir}/gvfsd-computer
%{_libexecdir}/gvfsd-dav
%{_libexecdir}/gvfsd-dnssd
%{_libexecdir}/gvfsd-ftp
%{_libexecdir}/gvfsd-http
%{_libexecdir}/gvfsd-localtest
%{_libexecdir}/gvfsd-metadata
%{_libexecdir}/gvfsd-network
%{_libexecdir}/gvfsd-sftp
%{_libexecdir}/gvfsd-trash
%{_datadir}/dbus-1/services/gvfs-daemon.service
%{_datadir}/dbus-1/services/gvfs-metadata.service
%{_datadir}/dbus-1/services/org.gtk.Private.GduVolumeMonitor.service
%dir %{_datadir}/gvfs
%dir %{_datadir}/gvfs/mounts
%dir %{_datadir}/gvfs/remote-volume-monitors
%{_datadir}/gvfs/remote-volume-monitors/gdu.monitor
%{_datadir}/gvfs/mounts/afp-browse.mount
%{_datadir}/gvfs/mounts/afp.mount
%{_datadir}/gvfs/mounts/burn.mount
%{_datadir}/gvfs/mounts/cdda.mount
%{_datadir}/gvfs/mounts/computer.mount
%{_datadir}/gvfs/mounts/dav.mount
%{_datadir}/gvfs/mounts/dav+sd.mount
%{_datadir}/gvfs/mounts/dns-sd.mount
%{_datadir}/gvfs/mounts/ftp.mount
%{_datadir}/gvfs/mounts/http.mount
%{_datadir}/gvfs/mounts/localtest.mount
%{_datadir}/gvfs/mounts/network.mount
%{_datadir}/gvfs/mounts/sftp.mount
%{_datadir}/gvfs/mounts/trash.mount
%{_datadir}/GConf/gsettings/gvfs-dns-sd.convert
%{_datadir}/glib-2.0/schemas/org.gnome.system.dns_sd.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.system.gvfs.enums.xml

%files -n %{libname}
%{_libdir}/libgvfscommon.so.%{major}*
%{_libdir}/libgvfscommon-dnssd.so.%{major}*

%files -n %{develname}
%doc NEWS ChangeLog AUTHORS TODO
%{_libdir}/lib*.so
%{_includedir}/gvfs-client

%files fuse
%{_libexecdir}/gvfs-fuse-daemon

%files smb
%{_libexecdir}/gvfsd-smb
%{_libexecdir}/gvfsd-smb-browse
%{_datadir}/gvfs/mounts/smb-browse.mount
%{_datadir}/gvfs/mounts/smb.mount

%files archive
%{_libexecdir}/gvfsd-archive
%{_datadir}/gvfs/mounts/archive.mount

%files obexftp
%{_libexecdir}/gvfsd-obexftp
%{_datadir}/gvfs/mounts/obexftp.mount

%if %{enable_gphoto2}
%files gphoto2
%{_libexecdir}/gvfsd-gphoto2
%{_datadir}/gvfs/mounts/gphoto2.mount
%{_libexecdir}/gvfs-gphoto2-volume-monitor
%{_datadir}/dbus-1/services/org.gtk.Private.GPhoto2VolumeMonitor.service
%{_datadir}/gvfs/remote-volume-monitors/gphoto2.monitor
%endif

%if %{enable_iphone}
%files iphone
%{_libexecdir}/gvfs-afc-volume-monitor
%{_libexecdir}/gvfsd-afc
%{_datadir}/dbus-1/services/org.gtk.Private.AfcVolumeMonitor.service
%{_datadir}/gvfs/mounts/afc.mount
%{_datadir}/gvfs/remote-volume-monitors/afc.monitor
%endif

