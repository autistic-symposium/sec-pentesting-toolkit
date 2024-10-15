# Grub Configuration

## Understanding MBR and EFI

BIOS/MBR is an older partition table type also referred to as Legacy mode. Nowadays, UEFI is in most of the new computer (especially those that came with W8 or W8.1 pre-installed). UEFI always use the gpt partition table type.

To find out each one your computer uses, you can boot into your computers Bios/firmware. Besides, to see if it is UEFI:

```
$ efibootmgr 
```

In a UEFI install, the ```grub.cfg``` file belongs in ```/boot/efi/EFI/fedora/grub.cfg```. In a msdos/MBR install, ```grub.cfg``` belongs in ```/boot/grub2/grub.cfg```.

Extra: to see your partitions, you can type:
```
$ gdisk -l /dev/sda 
```

## Modifying Grub Options

Edit ```/etc/default/grub```. For example, setting:

```
GRUB_DEFAULT="0"
```

After that, type the ```grub2-mkconfig``` command. In a MBR boot:

```
$ grub2-mkconfig -o /boot/grub2/grub.cfg
```

In an EFI boot:
```
$ grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg
```