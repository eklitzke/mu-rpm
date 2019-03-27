%define guiledir %{_datadir}/guile/2.2
%define baseversion 1.2
%define candidate rc1

Name:    mu-mail
Version: %{baseversion}~%{candidate}
Release: 1%{?dist}
Summary: mu: maildir indexing service
Group:   Applications/Internet
License: GPL v3.0
URL:     https://www.djcbsoftware.nl/code/mu/
Source0: https://github.com/djcb/mu/archive/%{baseversion}-%{candidate}.tar.gz

Patch1:  0001-mu4e-doc-dir.patch
Patch2:  0002-guile-installation-dir.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: emacs
BuildRequires: emacs-common
BuildRequires: emacs-el
BuildRequires: gcc-c++
BuildRequires: gmime30-devel
BuildRequires: guile22-devel
BuildRequires: libtool
BuildRequires: m4
BuildRequires: texinfo
BuildRequires: xapian-core-devel

Requires:      gmime30
Requires:      xapian-core-libs

%description
mu mail indexing service

%package guile
Summary:       Guile language bindings for mu
Group:         Applications/Internet
Requires:      gnuplot
Requires:      guile22
Requires:      %{name} = %{version}-%{release}
Enhances:      %{name} = %{version}-%{release}

%description guile
guile bindings for mu

%package -n emacs-mu4e
Summary:       GNU Emacs support for mu
Group:         Applications/Editors
BuildArch:     noarch
Requires:      emacs(bin) >= %{_emacs_version}
Requires:      emacs-filesystem >= %{_emacs_version}
Requires:      %{name} = %{version}-%{release}
Enhances:      %{name} = %{version}-%{release}

%description -n emacs-mu4e
emacs support for mu

%prep
%setup -q -n mu-%{baseversion}-%{candidate}
%patch1 -p1
%patch2 -p1

%build
./autogen.sh  # needed because we patched automakefiles
%configure --disable-gtk --disable-webkit
%make_build

%check
make check

%install
make install DESTDIR=%{buildroot}

# fix up mu4e texinfo docs
gzip -9 <mu4e/mu4e.info >%{buildroot}%{_infodir}/mu4e.info.gz
rm -f %{buildroot}%{_datadir}/doc/mu/mu4e-about.org
rm -f %{buildroot}%{_datadir}/doc/mu/NEWS.org
rm -f %{buildroot}%{_infodir}/dir

%clean
rm -rf %{buildroot}

%post -n emacs-mu4e
/sbin/install-info %{_infodir}/mu4e.info.gz %{_infodir}/dir

%preun -n emacs-mu4e
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/mu4e.info.gz %{_infodir}/dir
fi

%post guile
/sbin/install-info %{_infodir}/mu-guile.info.gz %{_infodir}/dir

%preun guile
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/mu-guile.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS NEWS NEWS.org README
%license COPYING
%{_bindir}/mu
%{_mandir}/man1/mu*.gz
%{_mandir}/man5/mu*.gz
%{_mandir}/man7/mu*.gz

%files guile
%license COPYING
%{_libdir}/libguile-mu.*
%{guiledir}/mu.scm
%{guiledir}/mu/*.scm
%{_datadir}/mu/scripts/*.scm
%{_infodir}/mu-guile.info.gz

%files -n emacs-mu4e
%doc AUTHORS NEWS NEWS.org README mu4e/mu4e-about.org
%license COPYING
%{_emacs_sitelispdir}/mu4e
%{_infodir}/mu4e.info.gz

%changelog
* Wed Mar 27 2019 Evan Klitzke <evan@eklitzke.org> - 1.2~rc1-1
- Actually use the official 1.2-rc1 tarball

* Wed Mar 27 2019 Evan Klitzke <evan@eklitzke.org> - 1.1.0-git20190324.1
- Auto update with changes in master, new git commit 51be30ad

* Mon Mar 04 2019 Evan Klitzke <evan@eklitzke.org> - 1.1.0-git20190302.1
- Auto update with changes in master, new git commit f9b615c3

* Mon Feb 25 2019 Evan Klitzke <evan@eklitzke.org> - 1.1.0-git20190225.1
- Auto update with changes in master, new git commit 31f73b32

* Mon Feb 18 2019 Evan Klitzke <evan@eklitzke.org> - 1.1.0-git20190218.1
- Update for changes in master; notably this updates to gmime30 and guile22

* Sat Oct 20 2018 Evan Klitzke <evan@eklitzke.org> - 1.0-9
- Rename package to mu-mail to avoid conflict with upstream mu package

* Sat Oct 20 2018 Evan Klitzke <evan@eklitzke.org> - 1.0-7
- Rebuilt for Fedora 29

* Wed Jun 06 2018 Evan Klitzke <evan@eklitzke.org> - 1.0-6
- Bump spec for Emacs 26.1

* Sun Mar 18 2018 Evan Klitzke <evan@eklitzke.org> - 1.0-5
- Install the guile scripts to the correct location.

* Sun Mar 18 2018 Evan Klitzke <evan@eklitzke.org> - 1.0-4
- Fix link to mu4e-about.org

* Sun Mar 18 2018 Evan Klitzke <evan@eklitzke.org> - 1.0-3
- Add mu-guile package

* Sun Mar 18 2018 Evan Klitzke <evan@eklitzke.org> - 1.0-2
- Clean up some minor packaging errors

* Sat Mar 17 2018 Evan Klitzke <evan@eklitzke.org> - 1.0-1
- Initial package
