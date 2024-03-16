# tpm12-crypt

This is a modified version of the crypt dracut module from systemd to add support to TPM1.2 with password.

## References

This is based on the following project:

- https://github.com/systemd/systemd
- https://github.com/gastamper/dracut-tpm
- https://github.com/archont00/arch-linux-luks-tpm-boot/

## Highlights

* Only TPM 1.2, with a password
* Dracut
* Standard [GNU GRUB](https://www.gnu.org/software/grub/index.html)
* If reading LUKS key from TPM fails, systemd prompts the user for LUKS passphrase on console

## Install

#### 0. backup
First of all, backup your current initramfs:

```console
/boot/distrib/ # cp initramfs-version.x86_64.img initramfs-version.x86_64.img.bak
```

#### 1. Install

* For fedora (and probably other distribution using rpm):
  * Download the latest rpm package: [releases](https://github.com/p1gp1g/dracut-tpm12-crypt/releases)
  * Install : `dnf install dracut-tpm12-crypt-{version}.rpm` or, if your system uses rpm-ostree, like Fedora Silverblue: `rpm-ostree install dracut-tpm12-crypt-{version}.rpm`
* For other distributions:
  * Install `trousers` and `tpm-tools`
  * Copy the config file and the module:
```console
# cp tpm12-crypt.conf /usr/lib/dracut/dracut.conf.d/
# cp -r 90tpm12-crypt /usr/lib/dracut/modules.d/
```

#### 2. Update your initramfs

* If your system doesn't use rpm-ostree:
```console
/boot/distrib/ # dracut -f initramfs-version.x86_64.img
```

* Else, if it uses rpm-ostree:
```console
# rpm-ostree initramfs --enable
# rpm-ostree initramfs --enable --arg=-f # if you need to reinstall and you already have enable local generation
```

#### 3. Reboot

To see if everything is working.

If your system can't boot, restore the previous initramfs using the emergency shell:

```console
# mkdir /mnt
# mount /dev/sda2 /mnt # change sda2 if needed
# cd /mnt/distrib
# cp initramfs-version.x86_64.img.bak initramfs-version.x86_64.img
# reboot
```

## Few notes on TPM

The LUKS key will be stored in TPM NVRAM and the TPM will be able to give out the LUKS key with a password.

This is done by:
* Setting an owner password for TPM device (necessary - needed for storing & sealing to NVRAM).
* Storing the LUKS key to TPM NVRAM area with a NVRAM password.

Owner password and NVRAM password can be different, the NVRAM password will be the one to enter on boot.

## Configuring TPM device

You'll have to take ownership of your TPM in case you haven't done so yet. You might be required to clear your TPM before you do this. Unfortunately, there is no defined way of how to do this, it depends on the hardware you are using. You'll probably be able to reset the TPM in your BIOS – for the systems I have seen so far, you can find the TPM settings under `Security` or `Onboard devices`. If not, you might want to look up a guide on how to reset the TPM on your hardware. Also be carefull if you use multiboot with another operating system which might rely on TPM, too.

First, take ownership of the TPM:

```console
# tpm_takeownership
```

Then, add a new keyfile to LUKS:

```console
# # Create a 1MB RAMFS to hold our data
# mkdir -p /mnt/ramfs
# mount -t tmpfs -o size=1m tmpfs /mnt/ramfs
# # Generate 256 bytes of random data to serve as our key
# dd if=/dev/random of=/mnt/ramfs/key bs=1 count=256
# # Define a new NVRAM area at the specified index, of the specified size
# # See 'man tpm_nvdefine' for permissions explanation
# tcsd
# tpm_nvdefine -i 1 -s 256 -p "OWNERWRITE|OWNERREAD" -o <owner_password> [-r <PCR1> -r <PCR2> ... n]
# # Write the data to index 1, size 256
# tpm_nvwrite -i 1 -s 256 -f /mnt/ramfs/key -p
# cryptsetup luksAddKey /dev/sda3 /mnt/ramfs/key
# # Unmount RAMFS
# umount /mnt/ramfs
```

You should be able to reboot and use the NVRAM password during boot time to decrypt your LUKS device.

With *Echap* during the plymouth splash screen, you can get more information about what is going on.

