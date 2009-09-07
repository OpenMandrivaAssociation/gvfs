%define name gvfs
%define version 1.3.6
%define release %mkrel 1

%define major 0
%define libname %mklibname %name %major
%define develname %mklibname -d %name

%define enable_gphoto2 1
%define enable_iphone 1

%define enable_gdu 0

Summary: Glib VFS library
Name: %{name}
Version: %{version}
Release: %{release}
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
Source1: bash-completion
Patch: 0001-Add-AFC-backend.patch
# (fc) 0.1.11-3mdv allow to show mount points in /mnt if they are ntfs or vfat
Patch1: gvfs-0.1.11-showmnt.patch
License: LGPLv2+
Group: System/Libraries
Url: http://www.gnome.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libhal-devel
BuildRequires: libgudev-devel
BuildRequires: libcdio-devel
BuildRequires: fuse-devel
BuildRequires: libsmbclient-devel
BuildRequires: libsoup-devel >= 2.23.91
BuildRequires: glib2-devel >= 2.21.5
#gw too late for 2008.1
%if %mdkversion > 200810
BuildRequires: libarchive-devel
%endif
BuildRequires: libGConf2-devel
BuildRequires: intltool
%if %{enable_gphoto2}
BuildRequires: gphoto2-devel
%endif
%if %{enable_iphone}
BuildRequires: libiphone-devel
%endif
BuildRequires: gnome-keyring-devel
BuildRequires: avahi-glib-devel
BuildRequires: avahi-client-devel
BuildRequires: bluez-devel
BuildRequires: dbus-glib-devel
BuildRequires: expat-devel
BuildRequires: gtk-doc
%if %{enable_gdu}
BuildRequires: libgdu-devel >= 0.4
%endif
#gw the dbus service depends on the daemon in the library package
Requires: %libname = %version
Requires: gnome-mount
Suggests: %name-fuse
Suggests: %name-smb
Suggests: %name-archive
#Suggests: %name-obexftp
%if %{enable_gphoto2}
#Suggests: %name-gphoto2
%endif

%description
This is a Virtual File System library based on gio and Glib.

%package -n %{libname}
Group: System/Libraries
Summary: Glib VFS library
Requires: %name >= %version

%description -n %{libname}
This is a Virtual File System library based on gio and Glib.

%package -n %develname
Group: Development/C
Summary: Glib VFS Library - development files
Requires: %libname = %version
Provides: libgvfs-devel = %version-%release

%description -n %develname
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
%patch -p1
cd monitor
%patch1 -p1 -b .showmnt
cd -
autoreconf -fi

%build
%configure2_5x \
%if %{enable_gphoto2}
 --enable-gphoto2
%else
 --disable-gphoto2
%endif

%make

%install
rm -rf %{buildroot}
%makeinstall_std
rm -f %buildroot%_libdir/gio/modules/*.la

%find_lang gvfs

# upstream bash completion is installed in the wrong place, with the wrong perms
# and redefine system variables without notice
rm -f %buildroot%_sysconfdir/profile.d/gvfs-bash-completion.sh
install -d -m 755 %buildroot%_sysconfdir/bash_completion.d
install -m 644 %{SOURCE1} %buildroot%_sysconfdir/bash_completion.d/%{name}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files -f gvfs.lang
%defattr(-,root,root)
%_sysconfdir/bash_completion.d/gvfs
%_bindir/gvfs-*
%_datadir/dbus-1/services/gvfs-daemon.service
%_datadir/dbus-1/services/gvfs-metadata.service
%_datadir/dbus-1/services/org.gtk.Private.HalVolumeMonitor.service
%if %{enable_gdu}
%_datadir/dbus-1/services/org.gtk.Private.GduVolumeMonitor.service
%endif
%dir %_datadir/gvfs
%dir %_datadir/gvfs/mounts
%dir %_datadir/gvfs/remote-volume-monitors
%_datadir/gvfs/remote-volume-monitors/hal.monitor
%if %{enable_gdu}
%_datadir/gvfs/remote-volume-monitors/gdu.monitor
%endif
%_datadir/gvfs/mounts/sftp.mount
%_datadir/gvfs/mounts/trash.mount
%_datadir/gvfs/mounts/cdda.mount
%_datadir/gvfs/mounts/computer.mount
%_datadir/gvfs/mounts/dav.mount
%_datadir/gvfs/mounts/dav+sd.mount
%_datadir/gvfs/mounts/http.mount
%_datadir/gvfs/mounts/localtest.mount
%_datadir/gvfs/mounts/burn.mount
%_datadir/gvfs/mounts/dns-sd.mount
%_datadir/gvfs/mounts/network.mount
%_datadir/gvfs/mounts/ftp.mount

%files -n %libname
%defattr(-,root,root)
%_libdir/gio/modules/libgiogconf.so
%_libdir/gio/modules/libgioremote-volume-monitor.so
%_libdir/gio/modules/libgvfsdbus.so
%if %{enable_gdu}
%_libexecdir/gvfs-gdu-volume-monitor
%endif
%_libexecdir/gvfs-hal-volume-monitor
%_libexecdir/gvfsd
%_libexecdir/gvfsd-ftp
%_libexecdir/gvfsd-metadata
%_libexecdir/gvfsd-sftp
%_libexecdir/gvfsd-trash
%_libexecdir/gvfsd-cdda
%_libexecdir/gvfsd-computer
%_libexecdir/gvfsd-dav
%_libexecdir/gvfsd-http
%_libexecdir/gvfsd-localtest
%_libexecdir/gvfsd-burn
%_libexecdir/gvfsd-dnssd
%_libexecdir/gvfsd-network
%_libdir/libgvfscommon.so.%{major}*
%_libdir/libgvfscommon-dnssd.so.%{major}*

%files -n %develname
%defattr(-,root,root)
%doc NEWS ChangeLog AUTHORS TODO
%_libdir/lib*.so
%_libdir/lib*.la
#%_includedir/%name/
%_includedir/gvfs-client
#%_libdir/pkgconfig/%name*.pc
#%doc %_datadir/gtk-doc/html/%name

%files fuse
%defattr(-, root, root, -)
%{_libexecdir}/gvfs-fuse-daemon


%files smb
%defattr(-, root, root, -)
%{_libexecdir}/gvfsd-smb
%{_libexecdir}/gvfsd-smb-browse
%{_datadir}/gvfs/mounts/smb-browse.mount
%{_datadir}/gvfs/mounts/smb.mount


%files archive
%defattr(-, root, root, -)
#%dir %{_datadir}/applications/mount-archive.desktop
%{_libexecdir}/gvfsd-archive
%{_datadir}/gvfs/mounts/archive.mount


%files obexftp
%defattr(-, root, root, -)
%{_libexecdir}/gvfsd-obexftp
%{_datadir}/gvfs/mounts/obexftp.mount

%if %{enable_gphoto2}
%files gphoto2
%defattr(-, root, root, -)
%{_libexecdir}/gvfsd-gphoto2
%{_datadir}/gvfs/mounts/gphoto2.mount
%{_libexecdir}/gvfs-gphoto2-volume-monitor
%{_datadir}/dbus-1/services/org.gtk.Private.GPhoto2VolumeMonitor.service
%{_datadir}/gvfs/remote-volume-monitors/gphoto2.monitor
%endif

%if %{enable_iphone}
%files iphone
%defattr(-, root, root, -)
%_libexecdir/gvfs-afc-volume-monitor
%_libexecdir/gvfsd-afc
%_datadir/dbus-1/services/org.gtk.Private.AfcVolumeMonitor.service
%_datadir/gvfs/mounts/afc.mount
%_datadir/gvfs/remote-volume-monitors/afc.monitor
%endif
