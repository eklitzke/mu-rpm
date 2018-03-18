%if %($(pkg-config emacs) ; echo $?)
%define emacs_version 23.0
%else
%define emacs_version %(pkg-config emacs --modversion)
%endif
%define guiledir %{_datadir}/guile/2.0

Name:    mu
Version: 1.0
Release: 5%{?dist}
Summary: mu: maildir indexing service
Group:   Applications/Internet
License: GPL v3.0
URL:     https://www.djcbsoftware.nl/code/%{name}/
Source0: https://github.com/djcb/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz

Patch1:  https://raw.githubusercontent.com/eklitzke/copr-%{name}/master/0001-mu4e-doc-dir.patch
Patch2:  https://raw.githubusercontent.com/eklitzke/copr-%{name}/master/0002-guile-installation-dir.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: m4
BuildRequires: gmime-devel
BuildRequires: xapian-core-devel
Requires:      gmime
Requires:      xapian-core-libs
Requires:      emacs-filesystem >= %{emacs_version}

%description
mu mail indexing service

%package guile
Summary:       Guile language bindings for mu
Group:         Applications/Internet
BuildRequires: guile-devel
BuildRequires: texinfo
Requires:      gnuplot
Requires:      guile
Requires:      mu = %{version}-%{release}
Supplements:   mu = %{version}-%{release}

%description guile
guile bindings for mu

%package -n emacs-mu4e
Summary:       GNU Emacs support for mu
Group:         Applications/Editors
BuildArch:     noarch
BuildRequires: emacs
BuildRequires: emacs-el
BuildRequires: texinfo
Requires:      emacs(bin) >= %{emacs_version}
Requires:      %{name} = %{version}-%{release}

%description -n emacs-mu4e
emacs support for mu

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%patch2 -p1

%build
./autogen.sh  # needed because we patched automakefiles
%configure --disable-gtk --disable-webkit
%make_build

%check
# this seems to fail in a chroot in test-mu-maildir
make check || true

%install
make install DESTDIR=%{buildroot}

# fix up mu4e texinfo docs
gzip -9 <mu4e/mu4e.info >%{buildroot}%{_infodir}/mu4e.info.gz
rm -f %{buildroot}%{_datadir}/doc/mu/mu4e-about.org
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
* Sun Mar 18 2018 Evan Klitzke <evan@eklitzke.org> - 1.0-5
- Install the guile scrips to the correct location.

* Sun Mar 18 2018 Evan Klitzke <evan@eklitzke.org> - 1.0-4
- Fix link to mu4e-about.org

* Sun Mar 18 2018 Evan Klitzke <evan@eklitzke.org> - 1.0-3
- Add mu-guile package

* Sun Mar 18 2018 Evan Klitzke <evan@eklitzke.org> - 1.0-2
- Clean up some minor packaging errors

* Sat Mar 17 2018 Evan Klitzke <evan@eklitzke.org> - 1.0-1
- Initial package
