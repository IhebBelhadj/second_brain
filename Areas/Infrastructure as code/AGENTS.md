# Area guide: Infrastructure as code

**Index:** `Infrastructure as code.md` is the learning path with a one-line summary of every note and the planned notes as italic links. Read it for *what* a note covers; use this file for *where* it is.

**Scope:** defining infrastructure in code a systems engineer reviews, versions and applies: Terraform first (syntax, state, modules, environments, testing, running it in production), then the neighbours (CloudFormation, Pulumi, Ansible, GitOps). The tools are vendor-neutral, but a tool needs a provider to show anything real: examples use the **AWS provider** (the current certification), with the shared "Acme shop" scenario. AWS service details stay in the AWS area and are linked, not re-explained.

## Folder map

```
Infrastructure as code/
├── Infrastructure as code.md      topic index (the learning path)
└── Terraform/                     Terraform from zero to production, in reading order
    ├── Infrastructure as code › Terraform.md   sub-topic index
    ├── Terraform.md               the entry point: console → scripts → declarative, init/plan/apply/destroy, plan symbols, how it works, vs other tools
    ├── Terraform language syntax.md          HCL: blocks, types, expressions, for/splat, functions, dynamic blocks, file layout
    ├── Terraform variables, locals and outputs.md   inputs (types, validation, sensitive), tfvars and precedence, locals, outputs
    ├── Terraform resources and data sources.md      references and the graph, count/for_each, lifecycle, replacement, provisioners, data sources
    ├── Terraform providers.md     required_providers, version constraints, lock file, credentials, aliases (multi-region/account)
    ├── Terraform state.md         what state holds, S3 backend + locking, state commands, moved/import/removed, drift
    ├── Terraform modules.md       root vs child modules, sources and versions, module design, composition, registry modules
    ├── Terraform environments and project layout.md   workspaces vs directories, accounts per env, state layers, repo layouts
    ├── Terraform testing and validation.md   fmt/validate/tflint/scanners, conditions and checks, terraform test, policy as code
    ├── Terraform in production.md CI/CD with saved plans, OIDC roles, drift detection, upgrades, guardrails, failure modes
    └── Terraform worked example.md the Acme shop from an empty AWS account to prod, every file shown
```

## Sub-topics

Every note in this area has `subtopic: <index name>` in its frontmatter, and is linked from that sub-topic index (`type: subtopic`, tag `subtopic`). The area index `Infrastructure as code.md` links every sub-topic index in its "Sub-topics" section.

| Sub-topic index | Lives in | Covers |
|---|---|---|
| `Infrastructure as code › Terraform.md` | `Terraform/` | Terraform from the first `apply` to a team running it in production |

## Where a new note goes

| It's about… | Folder |
|---|---|
| Terraform (any feature, workflow or practice) | `Terraform/`, named `Terraform <thing>` |
| IaC ideas that aren't tied to one tool (declarative vs imperative, drift, immutable infrastructure) | Area root (create a `Foundations/` folder and sub-topic once there are 2+) |
| Another tool (Pulumi, Ansible, CloudFormation/CDK) | Its own folder once it has 2+ notes |
| An AWS service itself | The AWS area. [[Packer]] stays in `Areas/AWS/Compute/` |

The planned notes (roadmap) are the italic `*[[…]]*` links in `Infrastructure as code.md`: when writing one, use that exact name so existing links resolve.
