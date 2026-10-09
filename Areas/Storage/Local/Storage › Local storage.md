---
type: subtopic
created: 2026-10-09
topic: Storage
tags: [subtopic, storage]
---
# Storage › Local storage

> What this covers: one machine's storage: devices, partitions, filesystems, inodes, journaling, mounting, booting.

Part of [[Storage]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Storage devices]]: what a drive really is. HDD vs SSD (FTL, TRIM) vs the interface (SATA, NVMe), numbered blocks (LBA), block devices in `/dev`, the page cache and `fsync`, drives that aren't physical (loop devices, VM disks, EBS), a fake drive to practise on
- [[Partition tables (GPT and MBR)]]: how a drive is cut up, byte by byte. MBR's 512-byte sector (boot code, 4 entries, 55 AA, the 2 TiB limit, extended/logical chains), GPT (protective MBR, header with CRC, 128 entries with type and unique GUIDs, backup at the end), partition type GUIDs and real Windows/Linux/cloud layouts, PARTUUID vs UUID, repairing and converting
- [[Booting from disk]]: how firmware starts an OS. Legacy BIOS running sector 0 vs UEFI running `.efi` files from the **EFI system partition** (what an "EFI image on the disk" means), NVRAM boot entries and the fallback path, Secure Boot and shim, measured boot and BitLocker, initramfs and the root mount, UKIs, the Windows chain (bootmgfw, BCD, winload), boot failures
- [[Partitions and filesystems]]: from raw blocks to named files. GPT partitions, what `mkfs` lays out, inodes (no name inside), directories as name → inode lists, path lookup step by step, hard links, writing a file, journaling after a power cut, choosing ext4/XFS/btrfs/ZFS, inode exhaustion, deleted-but-open files, growing filesystems
- [[Inodes]]: the per-file record, drawn. Name / inode / data layers, every field and the four timestamps, block pointers (direct, indirect) vs extents, sparse files, hard and symbolic links, fd → open file → inode (deleted-but-open files, updating running programs), inode limits, how XFS, btrfs, FAT and NTFS differ
- [[Journaling]]: crash consistency. Why one save is many writes, what a crash leaves, fsck, journal transactions and the commit point, flushes and lying disks, data=journal/ordered/writeback, logical journaling, copy-on-write, log-structured, and the same write-ahead-log idea in databases, replication, CDC, Kafka, Raft, Redis, event sourcing and RAID
- [[Mounting]]: one tree vs drive letters, what `mount` does and hides, the VFS dispatching to ext4/NFS/proc/FUSE, mount options, `/etc/fstab` with UUIDs, virtual filesystems, bind mounts and container mount namespaces, busy unmounts, the mount that silently didn't happen
- [[How mounting works]]: under the hood. Why one kernel must own a device, type detection by magic numbers, the mount system calls, what the driver does (superblock, features, journal replay, root inode), superblock and mount objects, mountinfo, path walks crossing mount points, bind mounts sharing a superblock, unmounting, propagation, why two machines must never mount one disk, Windows' lazy mounting
- [[Windows vs Linux storage]]: the same topics on Windows. Disks/volumes/letters and the object namespace, Mount Manager and lazy mounting, NTFS's MFT vs inodes, $LogFile and the USN journal, ACLs vs mode bits, file-in-use locking, names and paths, links/reparse points, VSS, BitLocker, filter drivers, cross-OS data exchange, command translation

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
