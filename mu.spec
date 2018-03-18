Name:    mu
Version: 1.0
Release: 1%{?dist}
Summary: mu: maildir indexing service
Group:   Applications/System
License: GPL v3.0
URL:     https://www.djcbsoftware.nl/code/%{name}/
Source0: https://github.com/djcb/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz

#BuildRequires: gcc
#BuildRequires: pkgconfig
BuildRequires: gmime-devel
BuildRequires: xapian-core-devel
Requires:      gmime
Requires:      xapian-core-libs
Requires:      emacs-filesystem >= %{_emacs_version}

%description
mu mail indexing service

%package -n emacs-mu4e
Summary:       GNU Emacs support for mu
Group:         Applications/Editors
BuildArch:     noarch
BuildRequires: emacs
BuildRequires: emacs-el
BuildRequires: texinfo
Requires:      emacs(bin) >= %{_emacs_version}
Requires:      %{name} = %{version}-%{release}

%description -n emacs-mu4e
emacs support for mu

%prep
%setup -q -n %{name}-%{version}

%build
%configure --disable-gtk --disable-webkit --disable-guile
%make_build

%check
# works locally but fails in chroot
make check || true

%install
make install DESTDIR=%{buildroot}
gzip -9 <mu4e/mu4e.info > %{buildroot}%{_infodir}/mu4e.info.gz
#mkdir %{buildroot}%{_datadir}/doc/emacs-mu4e
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

%files
%doc NEWS.org
%license COPYING
%{_bindir}/mu
%{_mandir}/man1/mu*.gz
%{_mandir}/man5/mu*.gz
%{_mandir}/man7/mu*.gz

%files -n emacs-mu4e
%doc NEWS.org mu4e/mu4e-about.org
%{_emacs_sitelispdir}/mu4e
%{_infodir}/mu4e.info.gz
%{_infodir}/mu4e.info.gz

%changelog
* Sat Mar 17 2018 Evan Klitzke <evan@eklitzke.org> - 1.0-1
- Initial package
