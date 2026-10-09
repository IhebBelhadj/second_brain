---
type: subtopic
created: 2026-10-09
topic: AWS
tags: [subtopic, aws]
---
# AWS › Storage and databases

> What this covers: where data lives: S3, EFS, replication, RDS.

Part of [[AWS]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[S3]]: object storage. Buckets and keys (no real folders), storage classes and lifecycle, versioning, replication, who can access a bucket, presigned URLs, gateway endpoints, and the 403s
- [[S3 replication]]: CRR/SRR step by step (versioning, role, rule), Batch Replication for existing objects, cross-account (bucket policy, ownership), **which account needs which Region enabled** (the exam question), SSE-KMS, deletes and Object Lock, RTC, two-way, what isn't replicated, PENDING/FAILED debugging
- [[EFS]]: managed NFS for **Linux** clients (not Windows: FSx). Mount targets per AZ and port 2049, the mount helper (`-t efs`, `tls`, `iam`) vs plain `nfs4`, IAM authorization with a file system policy, access points for apps and containers, storage classes and throughput modes, EFS vs EBS vs S3 vs FSx, mount failures
- [[RDS]]: managed relational databases. What I give up (no SSH), Multi-AZ vs read replicas, failover through the endpoint, backups and point-in-time restore (always a new instance), RDS Proxy, Aurora, and the connection problems I'll debug
- CloudFront doesn't have its own note yet, and it shows up in almost every architecture (S3 and RDS done → [[S3]], [[RDS]])

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
