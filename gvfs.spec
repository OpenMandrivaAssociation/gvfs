%define major	0
%define libname %mklibname %{name}common %{major}
%define devname %mklibname -d %{name}common
%define gioname gio2.0

%define enable_gphoto2 1
%define enable_iphone 1

%define Werror_cflags %nil

Summary:	Glib VFS library
Name:		gvfs
Version:	1.17.1
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnome.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz
#gw from Ubuntu, fix music player detection
# https://bugs.freedesktop.org/show_bug.cgi?id=24500
Patch0:		gvfs-music-player-mimetype.patch
Patch1:		gvfs-1.13.4-glibh.patch

BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	xsltproc
BuildRequires:	cdda-devel
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(avahi-glib)
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gmodule-no-export-2.0)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(gudev-1.0) >= 186
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(libbluray)
BuildRequires:	pkgconfig(libcdio_paranoia)
BuildRequires:	pkgconfig(libmtp)
BuildRequires:	pkgconfig(libsoup-gnome-2.4)
BuildRequires:	pkgconfig(libsystemd-login)
BuildRequires:	pkgconfig(openobex)
BuildRequires:	pkgconfig(smbclient)
BuildRequires:	pkgconfig(udisks2)
%if %{enable_gphoto2}
BuildRequires:	pkgconfig(libgphoto2)
%endif
%if %{enable_iphone}
BuildRequires:	pkgconfig(libimobiledevice-1.0) >= 1.1.0
BuildRequires:	pkgconfig(libplist) >= 0.15
%endif

Requires(post,postun):	%{gioname} >= 2.23.4-2
Requires:	udisks2
Suggests:	%{name}-fuse
Suggests:	%{name}-smb
Suggests:	%{name}-archive
#Suggests:	%{name}-obexftp
%if %{enable_gphoto2}
Suggests:	%{name}-gphoto2
%endif
Conflicts:	%{libname} < 1.6.7-4
Conflicts:	%{name}-gphoto2 <= 1.13.2-2
Requires(post):	rpm-helper

%description
This is a Virtual File System library based on gio and Glib.

%package -n %{libname}
Group:		System/Libraries
Summary:	Glib VFS library
Obsoletes:	%{_lib}gvfs0 < 1.15.4-2

%description -n %{libname}
This is a Virtual File System library based on gio and Glib.

%package -n %{devname}
Group:		Development/C
Summary:	Glib VFS Library - development files
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}gvfs-devel < 1.15.4-2

%description -n %{devname}
This is a Virtual File System library based on gio and Glib.

%package fuse
Summary:	FUSE support for gvfs
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	fuse

%description fuse
This package provides support for applications not using gio
to access the gvfs filesystems.

%package smb
Summary:	Windows fileshare support for gvfs
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description smb
This package provides support for reading and writing files on windows
shares (SMB) to applications using gvfs.

%package archive
Summary:	Archiving support for gvfs
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description archive
This package provides support for accessing files inside Zip and Tar archives,
as well as ISO images, to applications using gvfs.

%package obexftp
Summary:	ObexFTP support for gvfs
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	obex-data-server >= 0.3.4-6

%description obexftp
This package provides support for reading files on Bluetooth mobile phones
and devices through ObexFTP to applications using gvfs.

%package gphoto2
Summary:	gphoto2 support for gvfs
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description gphoto2
This package provides support for reading and writing files on
PTP based cameras (Picture Transfer Protocol) and MTP based
media players (Media Transfer Protocol) to applications using gvfs.

%package iphone
Summary:	iphone support for gvfs
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description iphone
This package provides support for reading and writing files on
the iPhone and the iPod TouchP to applications using gvfs.

%package mtp
Summary:	MTP support for gvfs
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description mtp
This package provides support for reading and writing files on
MTP based devices (Media Transfer Protocol) to applications using gvfs.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--with-dbus-service-dir=%{_datadir}/dbus-1/services \
	--disable-hal \
	--disable-gdu \
	--enable-udisks2 \
%if %{enable_gphoto2}
	--enable-gphoto2 \
%else
	--disable-gphoto2 \
%endif
	--enable-keyring

%make

%install
%makeinstall_std
%find_lang %{name}

# upstream bash completion is installed in the wrong place, with the wrong perms
# and redefine system variables without notice
rm -f %{buildroot}%{_sysconfdir}/profile.d/gvfs-bash-completion.sh

%post
systemd-tmpfiles --create gvfsd-fuse-tmpfiles.conf

%files -f %{name}.lang
%{_prefix}/lib/tmpfiles.d/gvfsd-fuse-tmpfiles.conf
%{_datadir}/bash-completion/completions/gvfs
%{_bindir}/gvfs-*
%{_libdir}/gio/modules/libgioremote-volume-monitor.so
%{_libdir}/gio/modules/libgvfsdbus.so
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
%{_libdir}/gvfs-udisks2-volume-monitor
%{_datadir}/dbus-1/services/gvfs-daemon.service
%{_datadir}/dbus-1/services/gvfs-metadata.service
%{_datadir}/dbus-1/services/org.gtk.Private.UDisks2VolumeMonitor.service
%dir %{_datadir}/gvfs
%dir %{_datadir}/gvfs/mounts
%dir %{_datadir}/gvfs/remote-volume-monitors
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
%{_datadir}/gvfs/remote-volume-monitors/udisks2.monitor
%{_mandir}/man1/gvfs*.1.*
%{_mandir}/man7/gvfs*.7.*

%files -n %{libname}
%{_libdir}/libgvfscommon.so.%{major}*

%files -n %{devname}
%doc NEWS ChangeLog AUTHORS TODO
%{_libdir}/lib*.so
%{_includedir}/gvfs-client

%files fuse
%{_libdir}/gvfsd-fuse

%files smb
%{_libexecdir}/gvfsd-smb
%{_libexecdir}/gvfsd-smb-browse
%{_datadir}/gvfs/mounts/smb-browse.mount
%{_datadir}/gvfs/mounts/smb.mount
%{_datadir}/GConf/gsettings/gvfs-smb.convert
%{_datadir}/glib-2.0/schemas/org.gnome.system.smb.gschema.xml

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

%files mtp
%{_libexecdir}/gvfs-mtp-volume-monitor
%{_libexecdir}/gvfsd-mtp
%{_datadir}/dbus-1/services/org.gtk.Private.MTPVolumeMonitor.service
%{_datadir}/gvfs/mounts/mtp.mount
%{_datadir}/gvfs/remote-volume-monitors/mtp.monitor
