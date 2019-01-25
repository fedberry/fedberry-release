%define release_name Twenty Nine
%define dist_version 29

Summary:    FedBerry release files
Name:       fedberry-release
Version:    29
Release:    2
License:    MIT
Group:      System Environment/Base
URL:        https://github.com/fedberry/fedberry-release
Source0:    %{url}/raw/master/LICENSE
Source1:    %{url}/raw/master/Fedora-Legal-README.txt
Source2:    %{url}/raw/master/85-display-manager.preset
Source3:    %{url}/raw/master/90-default.preset
Source4:    %{url}/raw/master/99-default-disable.preset
Source5:    %{url}/raw/master/90-default-user.preset
Source6:    https://github.com/fedberry/fedberry/raw/master/RELEASE-NOTES.md
Source7:    https://github.com/fedberry/fedberry/raw/master/README.md
Source8:    https://github.com/fedberry/fedberry/raw/master/INSTALL.md
BuildArch:  noarch
BuildRequires:  discount >= 2.1

Obsoletes:  redhat-release
Provides:   redhat-release
Provides:   fedora-release = %{version}-%{release}
Provides:   system-release
Provides:   system-release(%{version})
Requires:   fedora-repos
Requires:   fedberry-repo
Conflicts:  fedora-release
Obsoletes:  fedora-release


%description
FedBerry release files such as various /etc/ files that define the release.


%package notes
Summary:    Release Notes
License:    Open Publication
Group:      System Environment/Base
Provides:   system-release-notes = %{version}-%{release}
Conflicts:  fedora-release-notes

%description notes
FedBerry release notes package.


%prep
%setup -c -T
cp -a %{sources} .


%build
for MD_FILE in *.md; do
  markdown -o FedBerry-${MD_FILE%.*}.html ${MD_FILE}
done


%install
install -d %{buildroot}/etc
echo "FedBerry release %{version} (%{release_name})" > %{buildroot}/etc/fedora-release
echo "cpe:/o:fedberry:fedberry:%{version}" > %{buildroot}/etc/system-release-cpe
cp -p %{buildroot}/etc/fedora-release %{buildroot}/etc/issue
echo "Kernel \r on an \m (\l)" >> %{buildroot}/etc/issue
cp -p %{buildroot}/etc/issue %{buildroot}/etc/issue.net
echo >> %{buildroot}/etc/issue
ln -s fedora-release %{buildroot}/etc/redhat-release
ln -s fedora-release %{buildroot}/etc/system-release

mkdir -p %{buildroot}/usr/lib/systemd/system-preset/

cat << EOF >>%{buildroot}/usr/lib/os-release
NAME=FedBerry
VERSION="%{version} (%{release_name})"
ID=fedberry
ID_LIKE="rhel fedora"
VERSION_ID=%{version}
PRETTY_NAME="FedBerry (Fedora Remix) %{version} (%{release_name})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:fedberry:fedberry%{version}"
HOME_URL="https://fedberry.org"
BUG_REPORT_URL="https://github.com/fedberry"
EOF

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}/etc/os-release

# Set up the dist tag macros
install -d -m 755 %{buildroot}%{_rpmconfigdir}/macros.d
cat >> %{buildroot}%{_rpmconfigdir}/macros.d/macros.dist << EOF

# dist macros.
%%fedora    %{dist_version}
%%dist      .fc%{dist_version}
%%fc%{dist_version} 1
EOF

# Add presets
# Default system wide
install -m 0644 85-display-manager.preset %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 90-default.preset %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 90-default-user.preset %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 99-default-disable.preset %{buildroot}%{_prefix}/lib/systemd/system-preset/

%post
/usr/bin/systemctl enable dbus-daemon.service >/dev/null 2>&1 || :

%postun
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /usr/bin/systemctl enable dbus-daemon.service >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
%doc LICENSE Fedora-Legal-README.txt FedBerry-README.html
%config %attr(0644,root,root) /usr/lib/os-release
/etc/os-release
%config %attr(0644,root,root) /etc/fedora-release
/etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/90-default-user.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset


%files notes
%defattr(-,root,root,-)
%doc FedBerry-README.html FedBerry-RELEASE-NOTES.html FedBerry-INSTALL.html


%changelog
* Fri Jan 25 2019 Vaughan <devel at agrez dot net> - 29-2
- Update default presets for systemd

* Tue Oct 09 2018 Vaughan <devel at agrez dot net> - 29-1
- FedBerry 29 release

* Tue Jun 26 2018 Vaughan <devel at agrez dot net> - 28-1
- FedBerry 28 release
- Update spec

* Thu Nov 23 2017 Vaughan <devel at agrez dot net> - 27-1
- FedBerry 27 release

* Mon Jul 24 2017 Vaughan <devel at agrez dot net> - 26-2
- Update default systemd presets

* Sat Jul 08 2017 Vaughan <devel at agrez dot net> - 26-1
- FedBerry 26 release

* Thu Jun 01 2017 Vaughan <devel at agrez dot net> - 25-5
- Update spec source file links
- Rebuild to include updated readme, release-notes and install files

* Thu Feb 16 2017 Vaughan <devel at agrez dot net> - 25-4
- Rebuild to include updated readme, release-notes and install files

* Mon Jan 23 2017 Vaughan <devel at agrez dot net> - 25-3
- Update %%{release_name}

* Mon Jan 02 2017 Vaughan <devel at agrez dot net> - 25-2
- Simplify %%prep
- Bump release

* Mon Jan 02 2017 Vaughan <devel at agrez dot net> - 25-1
- New FedBerry release

* Fri Sep 16 2016 Vaughan <devel at agrez dot net> - 24-1
- Add Provides and Obsoletes: fedora-release

* Thu Sep 01 2016 Vaughan <devel at agrez dot net> - 24-0.4
- Pull in further release note updates

* Wed Jun 22 2016 Vaughan <devel at agrez dot net> - 24-0.3
- Rebuild to include updated readme, release-notes and install files.

* Wed Jun 22 2016 Vaughan <devel at agrez dot net> - 24-0.2
- Update default systemd presets

* Wed Jun 08 2016 Vaughan <devel at agrez dot net> - 24-0.1
- New FedBerry release

* Sun Mar 06 2016 mrjoshuap <jpreston at redhat dot com> - 23-0.9
- Autogenerate html docs from md files

* Thu Jan 28 2016 Vaughan <devel at agrez dot net> - 23-0.8
- Import & initial build for FedBerry

* Wed Jul 15 2015 Bruno Wolff III <bruno@wolff.to> - 23-0.7
- f23 has branched off from rawhide

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 23-0.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Dennis Gilmore <dennis@ausil.us> - 23-0.5
- add system preset files
- drop product sub-packages

* Sat Feb 14 2015 Bruno Wolff III <bruno@wolff.to> - 23-0.4
- Fix up change log

* Sat Feb 14 2015 Bruno Wolff III <bruno@wolff.to> - 23-0.3
- Rawhide is now 23

* Tue Oct 21 2014 Tom Callaway <spot@fedoraproject.org> - 22-0.3
- add versioned provide for system-release(VERSION)

* Tue Oct 21 2014 Tom Callaway <spot@fedoraproject.org> - 22-0.2
- add productization (it is the foooooture)

* Thu Aug 07 2014 Dennis Gilmore <dennis@ausil.us> - 22-0.1
- Require fedora-repos and no longer ship repo files

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Tom Callaway <spot@fedoraproject.org> - 21-4
- license changes and clarification doc

* Sun Mar 09 2014 Bruno Wolff III <bruno@wolff.to> - 21-3
- Install dist macro into the correct directory

* Sun Jan 05 2014 Bruno Wolff III <bruno@wolff.to> - 21-2
- Work around incorrect prefix in the upstream tarball

* Sun Jan 05 2014 Bruno Wolff III <bruno@wolff.to> - 21-1
- Bump version to match current rawhide

* Sat Dec 21 2013 Bruno Wolff III <bruno@wolff.to> - 21-0.3
- Update version to 21 (which should have happened when f20 was branched)
- Changed to work with recent yum change (bug 1040607)

* Mon Dec  9 2013 Tom Callaway <spot@fedoraproject.org> - 20-1
- final release (disable rawhide dep)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 26 2013 Tom Callaway <spot@fedoraproject.org> - 20-0.1
- sync

* Wed Jun 26 2013 Tom Callaway <spot@fedoraproject.org> - 19-2
- sync to release

* Mon Mar 11 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 19-0.3
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 19-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 19 2012 Tom Callaway <spot@fedoraproject.org> - 19-0.1
- sync to 19-0.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 18-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 10 2012 Tom Callaway <spot@fedoraproject.org> - 18-0.2
- sync with fedora-release model

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 28 2011 Tom Callaway <spot@fedoraproject.org> - 17-0.2
- initial 17

* Fri Jul 22 2011 Tom Callaway <spot@fedoraproject.org> - 16-0.2
- require -rawhide subpackage if we're built for rawhide

* Fri May 13 2011 Tom Callaway <spot@fedoraproject.org> - 16-0.1
- initial 16

* Fri May 13 2011 Tom Callaway <spot@fedoraproject.org> - 15-1
- sync to f15 final

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 15-0.3
- sync to rawhide

* Wed Feb 24 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 14-0.2
- fix broken requires

* Wed Feb 17 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 14-0.1
- update to sync with fedora-release

* Mon Nov 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 12-1
- Update for F12 final

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 11.90-1
- Build for F12 collection

* Wed May 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 11-1
- resync with fedora-release package

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> 10.90-2
- drop Requires: system-release-notes

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 10.90-1
- 10.90

* Thu Nov 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 10-1
- Bump to 10, update repos

* Mon Sep 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 9.91-2
- add Conflicts
- further sanitize descriptions

* Mon Sep 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 9.91-1
- initial package for generic-release and generic-release-notes
