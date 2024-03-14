%define dracutlibdir %{_prefix}/lib/dracut

Name:           dracut-tpm12-crypt
Version:        1.0
Release:        1%{?dist}
Summary:        A dracut module to decrypt a LUK2 disk on boot using a TPM1.2 with a password
BuildArch:      noarch

License:        LGPL-2.1-or-later
Source0:        %{name}-%{version}.tar.gz

Requires:       tpm-tools trousers

%description
This package contains a modified version of the crypt dracut module to work with TPM1.2 setup with a password.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/90tpm12-crypt
rm -f $RPM_BUILD_ROOT/%{dracutlibdir}/dracut.conf.d/90-tpm12-crypt.conf
mkdir -p $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d
mkdir -p $RPM_BUILD_ROOT/%{dracutlibdir}/dracut.conf.d
cp -r ./90tpm12-crypt/ $RPM_BUILD_ROOT/%{dracutlibdir}/modules.d/90tpm12-crypt
install -m 0644 ./tpm12-crypt.conf $RPM_BUILD_ROOT/%{dracutlibdir}/dracut.conf.d/90-tpm12-crypt.conf

%clean
rm -rf $RPM_BUILD_ROOT/%{dracutlibdir}/90tpm12-crypt
rm -f $RPM_BUILD_ROOT/%{dracutlibdir}/dracut.conf.d/90-tpm12-crypt.conf

%files
%dir %{dracutlibdir}/modules.d/90tpm12-crypt
%{dracutlibdir}/modules.d/90tpm12-crypt/crypt-cleanup.sh
%{dracutlibdir}/modules.d/90tpm12-crypt/crypt-lib.sh
%{dracutlibdir}/modules.d/90tpm12-crypt/cryptroot-ask.sh
%{dracutlibdir}/modules.d/90tpm12-crypt/crypt-run-generator.sh
%{dracutlibdir}/modules.d/90tpm12-crypt/module-setup.sh
%{dracutlibdir}/modules.d/90tpm12-crypt/parse-crypt.sh
%{dracutlibdir}/modules.d/90tpm12-crypt/parse-keydev.sh
%{dracutlibdir}/modules.d/90tpm12-crypt/probe-keydev.sh
%{dracutlibdir}/modules.d/90tpm12-crypt/tpm_unlock
%{dracutlibdir}/dracut.conf.d/90-tpm12-crypt.conf

%changelog
* Wed Mar 13 05:19:47 PM CET 2024 S1m <git@sgougeon.fr> - 1.0
- First version being packaged
