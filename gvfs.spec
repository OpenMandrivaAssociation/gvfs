%define name gvfs
%define version 0.1.8
%define release %mkrel 2

%define major 0
%define libname %mklibname %name %major
%define develname %mklibname -d %name

Summary: Glib VFS library
Name: %{name}
Version: %{version}
Release: %{release}
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
# (fc) 0.1.8-2mdv fix dav backend (SVN)
Patch0: gvfs-libxml.patch
License: LGPLv2+
Group: System/Libraries
Url: http://www.gnome.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libhal-devel
BuildRequires: libcdio-devel
BuildRequires: fuse-devel
BuildRequires: libsmbclient-devel
BuildRequires: libsoup-devel >= 2.3
BuildRequires: glib2-devel >= 2.15.6
BuildRequires: libGConf2-devel
BuildRequires: perl-XML-Parser
BuildRequires: gphoto2-devel
BuildRequires: gnome-keyring-devel
BuildRequires: avahi-glib-devel
BuildRequires: avahi-client-devel
BuildRequires: gtk-doc
BuildRequires: intltool
#gw the dbus service depends on the daemon in the library package
Requires: %libname = %version

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
%patch0 -p1 -b .libxml

#needed by patch0
autoreconf

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std
rm -f %buildroot%_libdir/gio/modules/*.la

%find_lang gvfs

%clean
rm -rf %{buildroot}

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files -f gvfs.lang
%defattr(-,root,root)
%_sysconfdir/profile.d/gvfs-bash-completion.sh
%_bindir/gvfs-*
%_datadir/dbus-1/services/gvfs-daemon.service
%dir %_datadir/gvfs
%dir %_datadir/gvfs/mounts
%_datadir/gvfs/mounts/*.mount

%files -n %libname
%defattr(-,root,root)
%_libdir/gio/modules/libgiogconf.so
%_libdir/gio/modules/libgiohal-volume-monitor.so
%_libdir/gio/modules/libgvfsdbus.so
%_libdir/gvfs-fuse-daemon
%_libdir/gvfsd*
%_libdir/libgvfscommon.so.%{major}*

%files -n %develname
%defattr(-,root,root)
%doc NEWS ChangeLog AUTHORS TODO
%_libdir/lib*.so
%_libdir/lib*.la
#%_includedir/%name/
%_includedir/gvfs-client
#%_libdir/pkgconfig/%name*.pc
#%doc %_datadir/gtk-doc/html/%name

