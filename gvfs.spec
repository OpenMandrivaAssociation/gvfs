%define name gvfs
%define version 1.1.8
%define release %mkrel 1

%define major 0
%define libname %mklibname %name %major
%define develname %mklibname -d %name

%define enable_gphoto2 0

Summary: Glib VFS library
Name: %{name}
Version: %{version}
Release: %{release}
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
Source1: bash-completion
# (fc) 0.1.11-3mdv allow to show mount points in /mnt if they are ntfs or vfat
Patch1: gvfs-0.1.11-showmnt.patch
License: LGPLv2+
Group: System/Libraries
Url: http://www.gnome.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libhal-devel
BuildRequires: libcdio-devel
BuildRequires: fuse-devel
BuildRequires: libsmbclient-devel
BuildRequires: libsoup-devel >= 2.23.91
BuildRequires: glib2-devel >= 2.19.1
#gw too late for 2008.1
%if %mdkversion > 200810
BuildRequires: libarchive-devel
%endif
BuildRequires: libGConf2-devel
BuildRequires: intltool
%if %{enable_gphoto2}
BuildRequires: gphoto2-devel
%endif
BuildRequires: gnome-keyring-devel
BuildRequires: avahi-glib-devel
BuildRequires: avahi-client-devel
BuildRequires: bluez-devel
BuildRequires: dbus-glib-devel
BuildRequires: expat-devel
BuildRequires: gtk-doc
#gw the dbus service depends on the daemon in the library package
Requires: %libname = %version
Requires: gnome-mount

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

%prep
%setup -q
cd monitor
%patch1 -p1 -b .showmnt
cd -

%build
%configure2_5x \
%if %{enable_gphoto2}
 --enable-gphoto2
%else
 --disable-gphoto2
%endif

#parallel build does not work
#http://bugzilla.gnome.org/show_bug.cgi?id=562955
make

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
%if %{enable_gphoto2}
%_datadir/dbus-1/services/org.gtk.Private.GPhoto2VolumeMonitor.service
%endif
%_datadir/dbus-1/services/org.gtk.Private.HalVolumeMonitor.service
%dir %_datadir/gvfs
%dir %_datadir/gvfs/mounts
%dir %_datadir/gvfs/remote-volume-monitors
%_datadir/gvfs/remote-volume-monitors/*.monitor
%_datadir/gvfs/mounts/*.mount

%files -n %libname
%defattr(-,root,root)
%_libdir/gio/modules/libgiogconf.so
%_libdir/gio/modules/libgioremote-volume-monitor.so
%_libdir/gio/modules/libgvfsdbus.so
%_libexecdir/gvfs-fuse-daemon
%if %{enable_gphoto2}
%_libexecdir/gvfs-gphoto2-volume-monitor
%endif
%_libexecdir/gvfs-hal-volume-monitor
%_libexecdir/gvfsd*
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

