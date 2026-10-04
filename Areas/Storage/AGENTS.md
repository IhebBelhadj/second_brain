# Area guide: Storage

**Index:** `Storage.md` is the learning path (7 numbered sections, each assumes the ones above) with a one-line summary of every note and the planned notes as italic links. Read it for *what* a note covers; use this file for *where* it is.

**Scope:** vendor-neutral storage for a systems engineer: block/file/object, devices and performance, filesystems, LVM, RAID, network storage, backups and replication, distributed storage. Cloud specifics live in `Areas/AWS/` and are linked from here, never mixed in (except a short "In the cloud" / "In AWS" section at the end of a note).

## Folder map

```
Storage/
├── Storage.md                     topic index (the learning path)
├── Foundations/
│   └── Storage devices.md         HDD/SSD/NVMe, LBA, block devices, page cache/fsync, loop devices, virtual drives
├── Local/
│   ├── Partitions and filesystems.md   GPT, mkfs layout, inodes, directories, path lookup, links, journaling, choosing, inode/space problems, growing
│   └── Mounting.md                one tree, mount/umount, VFS, options, fstab, virtual fs, bind mounts, namespaces, failures
└── Network storage/
    ├── NFS and SMB.md             exports/mounts, NFS versions, UID trust, SMB/Samba, cross-OS support, stale handles, hard/soft
    └── How network file sharing works.md   RPC, file handles, read/write paths, COMMIT, caching, leases/locks/delegations, SMB comparison
```

`S3.md`, `S3 replication.md` and `EFS.md` are listed in this area's index (section 7) but the files live in `Areas/AWS/Storage/` with `topic: AWS`.

## Where a new note goes

| It's about… | Folder |
|---|---|
| Storage types, devices, performance (section 1) | `Foundations/` |
| Partitions, filesystems, LVM, RAID (section 2) | `Local/` |
| NFS, SMB, iSCSI, SAN (section 3) | `Network storage/` |
| Object storage in general (section 4) | Area root |
| Backups, snapshots, replication, encryption at rest (section 5) | `Data protection/` |
| Distributed storage (section 6) | Area root, or a folder once 2+ notes share it |
| An AWS storage service (EBS, EFS, AWS Backup) | `Areas/AWS/Storage/`, `topic: AWS`, listed in section 7 of `Storage.md` |

Create a folder when its first note lands. The planned notes (roadmap) are the italic `*[[…]]*` links in `Storage.md`: when writing one, use that exact name so existing links resolve.
