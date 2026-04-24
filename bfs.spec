#
# Conditional build:
%bcond_without	acl		# POSIX ACL support
%bcond_without	cap		# Linux capability support
%bcond_without	selinux		# SELinux context support
%bcond_without	uring		# io_uring support
%bcond_without	oniguruma	# Oniguruma regex backend
%bcond_without	tests		# run the test suite

Summary:	Breadth-first version of the UNIX find command
Name:		bfs
Version:	4.1
Release:	1
License:	0BSD
Group:		Applications/File
#Source0Download: https://github.com/tavianator/bfs/releases
Source0:	https://github.com/tavianator/bfs/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	40397f6c724a1845016ff2367d20c3fe
URL:		https://bfs.tavianator.com/
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
%{?with_acl:BuildRequires:	acl-devel}
%{?with_cap:BuildRequires:	libcap-devel}
%{?with_oniguruma:BuildRequires:	oniguruma-devel}
%{?with_selinux:BuildRequires:	libselinux-devel}
%{?with_uring:BuildRequires:	liburing-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
bfs is a variant of the UNIX find command that operates
breadth-first rather than depth-first. It is otherwise intended to be
compatible with many versions of find, including POSIX find, GNU
find, BSD find, and macOS find.

%package -n bash-completion-%{name}
Summary:	bash-completion for bfs
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-%{name}
bash-completion for bfs.

%package -n fish-completion-%{name}
Summary:	fish-completion for bfs
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-%{name}
fish-completion for bfs.

%package -n zsh-completion-%{name}
Summary:	zsh-completion for bfs
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-%{name}
zsh-completion for bfs.

%prep
%setup -qc -n %{name}-%{version}

%build
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--enable-release \
	%{!?with_acl:--without-libacl} \
	%{!?with_cap:--without-libcap} \
	%{!?with_selinux:--without-libselinux} \
	%{!?with_uring:--without-liburing} \
	%{!?with_oniguruma:--without-oniguruma} \
	CC="%{__cc}" \
	EXTRA_CPPFLAGS="%{rpmcppflags}" \
	EXTRA_CFLAGS="%{rpmcflags}" \
	EXTRA_LDFLAGS="%{rpmldflags}"

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md docs/CHANGELOG.md docs/USAGE.md
%attr(755,root,root) %{_bindir}/bfs
%{_mandir}/man1/bfs.1*

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/bfs

%files -n fish-completion-%{name}
%defattr(644,root,root,755)
%{fish_compdir}/bfs.fish

%files -n zsh-completion-%{name}
%defattr(644,root,root,755)
%{zsh_compdir}/_bfs
