%define name gvfs
%define version 0.1.0
%define release %mkrel 2

%define major 0
%define libname %mklibname %name %major
%define develname %mklibname -d %name

Summary: Glib VFS library
Name: %{name}
Version: %{version}
Release: %{release}
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
# (fc) 0.1.0-2mdv update to latest SVN code
Patch0: gvfs-0.1.0-svn.patch
License: LGPLv2+
Group: System/Libraries
Url: http://www.gnome.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libhal-devel
BuildRequires: libcdio-devel
BuildRequires: fuse-devel
BuildRequires: libsmbclient-devel
BuildRequires: glib2-devel >= 2.15.1

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
%patch0 -p1 -b .svn

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
%dir %_sysconfdir/gvfs
%dir %_sysconfdir/gvfs/mounts
%config(noreplace) %_sysconfdir/gvfs/mounts/*.mount
%_bindir/gvfs-*
%_datadir/dbus-1/services/gvfs-daemon.service

%files -n %libname
%defattr(-,root,root)
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

