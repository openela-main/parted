Summary: The GNU disk partition manipulation program
Name:    parted
Version: 3.5
Release: 2%{?dist}
License: GPLv3+
URL:     http://www.gnu.org/software/parted

Source0: https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source1: https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz.sig
Source2: pubkey.phillip.susi
Source3: pubkey.brian.lane

# Upstream patches since v3.5 release
Patch0001: 0001-maint-post-release-administrivia.patch
Patch0002: 0002-parted-add-type-command.patch
Patch0003: 0003-libparted-add-swap-flag-for-DASD-label.patch
Patch0004: 0004-parted-Reset-the-filesystem-type-when-changing-the-i.patch
Patch0005: 0005-tests-t3200-type-change-now-passes.patch
Patch0006: 0006-libparted-Fix-handling-of-gpt-partition-types.patch
Patch0007: 0007-tests-Add-a-libparted-test-for-ped_partition_set_sys.patch
Patch0008: 0008-libparted-Fix-handling-of-msdos-partition-types.patch
Patch0009: 0009-tests-Add-a-libparted-test-for-ped_partition_set_sys.patch


BuildRequires: gcc
BuildRequires: e2fsprogs-devel
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: gettext-devel
BuildRequires: texinfo
BuildRequires: device-mapper-devel
BuildRequires: libuuid-devel
BuildRequires: libblkid-devel >= 2.17
BuildRequires: gnupg2
BuildRequires: git
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: e2fsprogs
BuildRequires: xfsprogs
BuildRequires: dosfstools
BuildRequires: perl-Digest-CRC
BuildRequires: bc
Buildrequires: python3
BuildRequires: gperf
BuildRequires: make
BuildRequires: check-devel

# bundled gnulib library exception, as per packaging guidelines
# https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries
Provides: bundled(gnulib)

%description
The GNU Parted program allows you to create, destroy, resize, move,
and copy hard disk partitions. Parted can be used for creating space
for new operating systems, reorganizing disk usage, and copying data
to new hard disks.


%package devel
Summary:  Files for developing apps which will manipulate disk partitions
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The GNU Parted library is a set of routines for hard disk partition
manipulation. If you want to develop programs that manipulate disk
partitions and filesystems using the routines provided by the GNU
Parted library, you need to install this package.


%prep
%autosetup -S git_am
gpg2 --import %{SOURCE2} %{SOURCE3}
gpg2 --verify %{SOURCE1} %{SOURCE0}
iconv -f ISO-8859-1 -t UTF8 AUTHORS > tmp; touch -r AUTHORS tmp; mv tmp AUTHORS

%build
# RHEL has 2.69 which works fine with the macros parted uses
sed -i s/2.71/2.69/ configure.ac
autoreconf -fiv
CFLAGS="$RPM_OPT_FLAGS -Wno-unused-but-set-variable"; export CFLAGS
%configure --disable-static --disable-gcc-warnings
# Don't use rpath!
%{__sed} -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
%{__sed} -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build


%install
%{__rm} -rf %{buildroot}
%make_install

# Remove components we do not ship
%{__rm} -rf %{buildroot}%{_libdir}/*.la
%{__rm} -rf %{buildroot}%{_infodir}/dir
%{__rm} -rf %{buildroot}%{_bindir}/label
%{__rm} -rf %{buildroot}%{_bindir}/disk

%find_lang %{name}


%check
export LD_LIBRARY_PATH=$(pwd)/libparted/.libs:$(pwd)/libparted/fs/.libs
make check

%files -f %{name}.lang
%doc AUTHORS NEWS README THANKS
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_sbindir}/parted
%{_sbindir}/partprobe
%{_mandir}/man8/parted.8.gz
%{_mandir}/man8/partprobe.8.gz
%{_libdir}/libparted.so.2
%{_libdir}/libparted.so.2.0.4
%{_libdir}/libparted-fs-resize.so.0
%{_libdir}/libparted-fs-resize.so.0.0.4
%{_infodir}/parted.info.*

%files devel
%doc TODO doc/API doc/FAT
%{_includedir}/parted
%{_libdir}/libparted.so
%{_libdir}/libparted-fs-resize.so
%{_libdir}/pkgconfig/libparted.pc
%{_libdir}/pkgconfig/libparted-fs-resize.pc


%changelog
* Tue Aug 09 2022 Brian C. Lane <bcl@redhat.com> - 3.5-2
- Fix ped_partition_set_system handling of existing flags
  Resolves: rhbz#2116505

* Fri May 27 2022 Brian C. Lane <bcl@redhat.com> - 3.5-1
- Rebase to upstream release 3.5
- Drop patches included in new upstream tar
- Add upstream patches for new type command
- Add upstream patch for swap flag on DASD
  Resolves: rhbz#1999333

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 3.4-6
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Tue Jun 15 2021 Brian C. Lane <bcl@redhat.com> - 3.4-5
- Install to /usr/sbin and /usr/lib64
  Resolves: rhbz#1972346

* Thu Jun 10 2021 Brian C. Lane <bcl@redhat.com> - 3.4-4
- Fix issues that covscan classifies as important
  Resolves: rhbz#1938836
- Work around a mkswap bug

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 3.4-3
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Wed Feb 03 2021 Brian C. Lane <bcl@redhat.com> - 3.4-2
- Add --fix support from upstream

* Wed Jan 27 2021 Brian C. Lane <bcl@redhat.com> - 3.4-1
- New stable upstream release v3.4

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 14 2020 Brian C. Lane <bcl@redhat.com> - 3.3.52-1
- New upstream ALPHA release v3.3.52
- Includes all patches

* Mon Nov 30 2020 Brian C. Lane <bcl@redhat.com> - 3.3-8
- Add upstream commits to fix various gcc 10 warnings (bcl)

* Thu Nov 05 2020 Brian C. Lane <bcl@redhat.com> - 3.3-7
- Do not link to libselinux

* Fri Sep 25 2020 Brian C. Lane <bcl@redhat.com> - 3.3-6
- tests: Add a test for resizepart on a busy partition (bcl)
- parted: Preserve resizepart End when prompted for busy partition (bcl)
- tests: Add f2fs to the fs probe test (romain.perier)
- Add support for the F2FS filesystem (romain.perier)
- Removed reference to ped_file_system_create (max)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 3.3-4
- Use make macros
  https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro
- Switch to using %%autosetup instead of %%setup and git (bcl)
- Update tests.yml to install git and simplify source usage (bgoncalv)

* Fri Mar 06 2020 Brian C. Lane <bcl@redhat.com> - 3.3-3
- Add chromeos_kernel partition flag for gpt disklabels
- Add bls_boot partition flag for msdos and gpt disklabels

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 16 2019 Brian C. Lane <bcl@redhat.com> - 3.3-2
- tests: Test incomplete resizepart command
- Fix end_input usage in do_resizepart
  Resolves: rhbz#1701411

* Fri Oct 11 2019 Brian C. Lane <bcl@redhat.com> - 3.3-1
- New upstream release v3.3
  Includes the DASD virtio-blk fix.
- Dropping pre-3.2 changelog entries
