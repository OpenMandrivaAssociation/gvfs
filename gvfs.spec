%define url_ver %(echo %{version}|cut -d. -f1,2)

%define major 0
%define devname %mklibname -d %{name}common
%define gioname gio2.0

%define enable_gphoto2 1
%define enable_iphone 1

%define Werror_cflags %nil

Summary:	Glib VFS library
Name:		gvfs
Version:	1.38.0
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnome.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gvfs/%url_ver/%{name}-%{version}.tar.xz
Patch1:		gvfs-1.13.4-glibh.patch

BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	xsltproc
BuildRequires:	cdda-devel
BuildRequires:	gettext-devel
BuildRequires:	meson
BuildRequires:	pkgconfig(avahi-glib)
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(gcr-base-3)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gmodule-no-export-2.0)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0
BuildRequires:	pkgconfig(gudev-1.0) >= 186
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(libbluray)
BuildRequires:	pkgconfig(libcap)
BuildRequires:	pkgconfig(libcdio_paranoia)
BuildRequires:	pkgconfig(libmtp)
BuildRequires:	pkgconfig(libnfs) >= 1.9.8
BuildRequires:	pkgconfig(libsoup-gnome-2.4)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(openobex)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(smbclient)
BuildRequires:	pkgconfig(udisks2)
BuildRequires:	pkgconfig(goa-1.0)
BuildRequires:	pkgconfig(libgdata)
%if %{enable_gphoto2}
BuildRequires:	pkgconfig(libgphoto2)
%endif
%if %{enable_iphone}
BuildRequires:	pkgconfig(libimobiledevice-1.0) >= 1.2.0
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
Conflicts:	%{name}-gphoto2 <= 1.13.2-2
Requires(post):	rpm-helper
%rename gvfs-obexftp

%description
This is a Virtual File System library based on gio and Glib.

%package -n %{devname}
Group:		Development/C
Summary:	Glib VFS Library - development files
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

%package gphoto2
Summary:	Gphoto2 support for gvfs
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description gphoto2
This package provides support for reading and writing files on
PTP based cameras (Picture Transfer Protocol) and MTP based
media players (Media Transfer Protocol) to applications using gvfs.

%package iphone
Summary:	Iphone support for gvfs
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
%meson -D systemduserunitdir=%{_userunitdir}
%meson_build

%install
%meson_install
%find_lang %{name}

# upstream bash completion is installed in the wrong place, with the wrong perms
# and redefine system variables without notice
rm -f %{buildroot}%{_sysconfdir}/profile.d/gvfs-bash-completion.sh

%files -f %{name}.lang
%{_prefix}/lib/tmpfiles.d/gvfsd-fuse-tmpfiles.conf
%{_libdir}/gio/modules/libgioremote-volume-monitor.so
%{_libdir}/gio/modules/libgvfsdbus.so
%{_libexecdir}/gvfsd
%{_libexecdir}/gvfsd-admin
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
%{_libexecdir}/gvfsd-nfs
%{_libexecdir}/gvfsd-recent
%{_libexecdir}/gvfsd-sftp
%{_libexecdir}/gvfsd-trash
%{_libexecdir}/gvfs-goa-volume-monitor
%{_libexecdir}/gvfsd-google
%{_libexecdir}/gvfs-udisks2-volume-monitor
%{_libdir}/gvfs/libgvfscommon.so
%{_libdir}/gvfs/libgvfsdaemon.so
%{_datadir}/gvfs/remote-volume-monitors/goa.monitor
%{_userunitdir}/gvfs-daemon.service
%{_userunitdir}/gvfs-metadata.service
%{_userunitdir}/gvfs-udisks2-volume-monitor.service
%{_userunitdir}/gvfs-goa-volume-monitor.service
%{_datadir}/dbus-1/services/org.gtk.vfs.UDisks2VolumeMonitor.service
%{_datadir}/dbus-1/services/org.gtk.vfs.Daemon.service
%{_datadir}/dbus-1/services/org.gtk.vfs.Metadata.service
%{_datadir}/dbus-1/services/org.gtk.vfs.GoaVolumeMonitor.service
%dir %{_datadir}/gvfs
%dir %{_datadir}/gvfs/mounts
%dir %{_datadir}/gvfs/remote-volume-monitors
%{_datadir}/gvfs/mounts/ftpis.mount
%{_datadir}/gvfs/mounts/google.mount
%{_datadir}/gvfs/mounts/admin.mount
%{_datadir}/gvfs/mounts/afp-browse.mount
%{_datadir}/gvfs/mounts/afp.mount
%{_datadir}/gvfs/mounts/burn.mount
%{_datadir}/gvfs/mounts/cdda.mount
%{_datadir}/gvfs/mounts/computer.mount
%{_datadir}/gvfs/mounts/dav.mount
%{_datadir}/gvfs/mounts/dav+sd.mount
%{_datadir}/gvfs/mounts/dns-sd.mount
%{_datadir}/gvfs/mounts/ftp.mount
%{_datadir}/gvfs/mounts/ftps.mount
%{_datadir}/gvfs/mounts/http.mount
%{_datadir}/gvfs/mounts/localtest.mount
%{_datadir}/gvfs/mounts/network.mount
%{_datadir}/gvfs/mounts/nfs.mount
%{_datadir}/gvfs/mounts/recent.mount
%{_datadir}/gvfs/mounts/sftp.mount
%{_datadir}/gvfs/mounts/trash.mount
%{_datadir}/GConf/gsettings/gvfs-dns-sd.convert
%{_datadir}/glib-2.0/schemas/org.gnome.system.dns_sd.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.system.gvfs.enums.xml
%{_datadir}/gvfs/remote-volume-monitors/udisks2.monitor
%{_datadir}/polkit-1/*/org.gtk.vfs.file-operations.*

%files -n %{devname}
%doc NEWS
%{_includedir}/gvfs-client

%files fuse
%{_libexecdir}/gvfsd-fuse

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

%if %{enable_gphoto2}
%files gphoto2
%{_libexecdir}/gvfsd-gphoto2
%{_datadir}/gvfs/mounts/gphoto2.mount
%{_libexecdir}/gvfs-gphoto2-volume-monitor
%{_datadir}/dbus-1/services/org.gtk.vfs.GPhoto2VolumeMonitor.service
%{_datadir}/gvfs/remote-volume-monitors/gphoto2.monitor
%{_userunitdir}/gvfs-gphoto2-volume-monitor.service
%endif

%if %{enable_iphone}
%files iphone
%{_libexecdir}/gvfs-afc-volume-monitor
%{_libexecdir}/gvfsd-afc
%{_datadir}/dbus-1/services/org.gtk.vfs.AfcVolumeMonitor.service
%{_datadir}/gvfs/mounts/afc.mount
%{_datadir}/gvfs/remote-volume-monitors/afc.monitor
%{_userunitdir}/gvfs-afc-volume-monitor.service
%endif

%files mtp
%{_libexecdir}/gvfs-mtp-volume-monitor
%{_libexecdir}/gvfsd-mtp
%{_datadir}/dbus-1/services/org.gtk.vfs.MTPVolumeMonitor.service
%{_datadir}/gvfs/mounts/mtp.mount
%{_datadir}/gvfs/remote-volume-monitors/mtp.monitor
%{_userunitdir}/gvfs-mtp-volume-monitor.service
