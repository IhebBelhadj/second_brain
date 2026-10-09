---
type: concept
created: 2026-10-09
topic: Infrastructure as code
subtopic: Infrastructure as code › Terraform
confidence: 1
tags: [iac, terraform, hcl, syntax]
aliases: [HCL, HashiCorp Configuration Language, Terraform syntax, Terraform expressions, Terraform functions]
---
# Terraform language syntax

> [!abstract] In one sentence
> Terraform code is written in HCL (HashiCorp Configuration Language): a small language made of **blocks** (`resource "type" "name" { … }`) holding **arguments** (`name = value`), where a value is an **expression** that can be a literal, a reference to something else, a function call, a conditional or a `for` loop over a collection. Everything else (types, strings, templates, splats, dynamic blocks) is a way of computing those values.

## Build-up: reading Acme's network code

The first config in [[Terraform]] was one bucket and one server, written with plain literals. Acme's real network code looks like this, and it's normal for it to look like noise at first:

```hcl
resource "aws_subnet" "private" {
  for_each          = { for i, az in local.azs : az => cidrsubnet(var.vpc_cidr, 8, i + 10) }
  vpc_id            = aws_vpc.main.id
  availability_zone = each.key
  cidr_block        = each.value
  tags              = merge(local.common_tags, { Name = "${local.prefix}-private-${each.key}" })
}
```

By the end of this note, every symbol in it reads as something specific. The build-up goes from the shape of a block, to values, to expressions that compute values.

## Stage 1: the shape of a block

Everything in a `.tf` file is a **block** or an **argument** inside a block.

```hcl
resource "aws_vpc" "main" {        # block type, then labels, then the body
  cidr_block           = "10.0.0.0/16"   # argument: name = expression
  enable_dns_hostnames = true

  tags = {                          # an argument whose value is a map
    Name = "shop-dev"
  }
}
```

| Part | In the example | What it is |
|---|---|---|
| Block type | `resource` | What kind of block (fixed keywords, list below) |
| Labels | `"aws_vpc"`, `"main"` | 0, 1 or 2 strings depending on the block type. For a resource: the resource type and my local name |
| Body | `{ … }` | Arguments and nested blocks |
| Argument | `cidr_block = "10.0.0.0/16"` | Assigns a value. Each argument name appears **once** per block |
| Nested block | `tags = { }` is an argument, but `ingress { }` (no `=`) is a nested block | Nested blocks can repeat; arguments can't |

The difference between `tags = { … }` (an **argument** holding a map, with `=`) and `ingress { … }` (a **nested block**, no `=`) matters: the provider's schema decides which one each name is, and using the wrong form is an error.

```hcl
resource "aws_security_group" "legacy" {
  name = "legacy"

  ingress {                 # nested block: repeatable
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### The block types

| Block | Labels | Does |
|---|---|---|
| `terraform` | none | Settings: `required_version`, `required_providers`, `backend` |
| `provider` | provider name (`"aws"`) | Configures a provider (region, credentials, tags). See [[Terraform providers]] |
| `resource` | type, name | Something Terraform creates and owns |
| `data` | type, name | Something Terraform only reads. See [[Terraform resources and data sources]] |
| `variable` | name | An input to the module |
| `locals` | none | Named intermediate values (`local.x`) |
| `output` | name | A value the module exposes. All three in [[Terraform variables, locals and outputs]] |
| `module` | name | Calls another module. See [[Terraform modules]] |
| `moved` | none | "This address was renamed": keeps the object instead of replacing it |
| `import` | none | "Adopt this existing object into this address" |
| `removed` | none | "Stop managing this, optionally without destroying it". These three in [[Terraform state]] |
| `check` | name | An assertion checked on every plan/apply that warns instead of failing. See [[Terraform testing and validation]] |
| `ephemeral` | type, name | A value fetched during the run and never written to state (Terraform 1.10+), e.g. a temporary secret |

### References: how blocks talk to each other

Each kind of block has its own reference syntax:

| Reference | Points to |
|---|---|
| `aws_vpc.main.id` | Attribute `id` of resource `aws_vpc` named `main` |
| `data.aws_availability_zones.available.names` | Attribute of a data source (prefix `data.`) |
| `var.vpc_cidr` | An input variable |
| `local.prefix` | A local value (note: block is `locals`, reference is `local.`) |
| `module.network.vpc_id` | An output of a module call |
| `each.key`, `each.value` | Inside a resource with `for_each` |
| `count.index` | Inside a resource with `count` |
| `path.module`, `path.root` | The folder of the current module / the root module |
| `terraform.workspace` | The current workspace name |
| `self` | The resource itself, only inside provisioners and some lifecycle conditions |

A reference is also a **dependency**: writing `aws_vpc.main.id` in the subnet is what tells Terraform to create the VPC (Virtual Private Cloud) first.

## Stage 2: values and types

Every value has a type. Terraform converts between them automatically when it's safe (the string `"5"` becomes the number `5` where a number is needed), and errors when it isn't.

| Type | Literal | Notes |
|---|---|---|
| `string` | `"eu-west-1"` | Always double quotes. Unicode text |
| `number` | `3`, `0.5`, `1e3` | One numeric type for integers and decimals |
| `bool` | `true`, `false` | |
| `list(T)` / `tuple([...])` | `["a", "b"]` | Ordered, indexed from 0: `var.azs[0]`. A list has one element type; a tuple's elements can each differ |
| `set(T)` | `toset(["a", "b"])` | Unordered, unique, **no index** |
| `map(T)` / `object({...})` | `{ Name = "web", Env = "dev" }` | Keys are always strings. A map has one value type; an object has a fixed set of named attributes, each with its own type |
| `null` | `null` | "No value": the argument is treated as **unset**, so the provider default applies |

The literal `{ … }` is an object and `[ … ]` is a tuple; they convert to `map` and `list` when assigned to something typed that way. Type constraints matter mostly for variables:

```hcl
variable "subnets" {
  type = map(object({
    cidr   = string
    public = optional(bool, false)   # optional attribute with a default
  }))
}
```

`null` is useful: "set this argument only in prod":

```hcl
resource "aws_instance" "web" {
  # ...
  key_name = var.environment == "prod" ? null : "debug-key"   # null = don't set it at all
}
```

## Stage 3: strings

```hcl
locals {
  prefix   = "${var.project}-${var.environment}"   # interpolation: "shop-dev"
  literal  = "costs $${amount}"                     # $${ escapes: the result is "costs ${amount}"
  path     = "C:\\temp\\x"                          # backslash escapes: \\ \" \n \t
}
```

`${ … }` inside a string evaluates any expression and inserts the result. A string that is **only** an interpolation, `"${var.x}"`, is the old Terraform 0.11 style: write `var.x`.

### Heredocs

For multi-line text (user data scripts, policies):

```hcl
resource "aws_instance" "web" {
  # ...
  user_data = <<-EOT
    #!/bin/bash
    echo "environment=${var.environment}" > /etc/shop.env
    dnf install -y nginx
  EOT
}
```

- `<<EOT … EOT` keeps the text exactly, indentation included
- `<<-EOT` (with the dash) strips the common leading indentation, so the heredoc can be indented with the code. Almost always the one to use
- `EOT` is just a marker; any word works (`EOF`, `POLICY`)

### Template directives

Inside strings and heredocs, `%{ … }` adds loops and conditionals:

```hcl
locals {
  allowed_ips = ["198.51.100.10", "198.51.100.11"]

  nginx_allow = <<-EOT
    %{ for ip in local.allowed_ips ~}
    allow ${ip};
    %{ endfor ~}
    deny all;
  EOT

  greeting = "Hello, %{ if var.environment == "prod" }customer%{ else }tester%{ endif }!"
}
```

Result of `nginx_allow`:
```
allow 198.51.100.10;
allow 198.51.100.11;
deny all;
```

The `~` **strip marker** removes the whitespace and newline next to it; without it, every `%{ for }` line leaves an empty line in the output. For anything longer than a few lines, I put the template in its own file and use `templatefile("${path.module}/nginx.conf.tftpl", { allowed_ips = local.allowed_ips })` (functions below).

## Stage 4: expressions that compute

### Operators

| Kind | Operators | Example |
|---|---|---|
| Arithmetic | `+ - * / %` | `var.replicas * 2` |
| Comparison | `== != < > <= >=` | `var.environment == "prod"` |
| Logical | `&& \|\| !` | `var.public && !var.internal` |

### Conditionals

`condition ? value_if_true : value_if_false`

```hcl
instance_type = var.environment == "prod" ? "m7i.large" : "t3.micro"
```

Both branches must have **compatible types**. `cond ? "a" : 5` errors with "Inconsistent conditional result types"; `cond ? [] : ["x"]` works because both are lists of strings once converted.

A very common idiom turns a resource **on or off** with `count`:

```hcl
resource "aws_cloudwatch_metric_alarm" "cpu" {
  count = var.environment == "prod" ? 1 : 0    # 0 instances = the resource doesn't exist
  # ...
}
```

## Stage 5: for expressions and splats

### for expressions

A `for` expression builds a new collection from another one. The **brackets** decide the result type:

```hcl
locals {
  azs = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]

  # [ ... ] produces a list
  upper_azs = [for az in local.azs : upper(az)]
  # => ["EU-WEST-1A", "EU-WEST-1B", "EU-WEST-1C"]

  # with the index
  numbered = [for i, az in local.azs : "${i}:${az}"]
  # => ["0:eu-west-1a", "1:eu-west-1b", "2:eu-west-1c"]

  # { k => v } produces a map (object)
  subnet_cidrs = { for i, az in local.azs : az => cidrsubnet("10.0.0.0/16", 8, i + 10) }
  # => { "eu-west-1a" = "10.0.10.0/24", "eu-west-1b" = "10.0.11.0/24", "eu-west-1c" = "10.0.12.0/24" }

  # filtering with if
  users = {
    alice = { team = "platform", admin = true }
    bob   = { team = "shop",     admin = false }
    carol = { team = "platform", admin = false }
  }
  admins = [for name, u in local.users : name if u.admin]
  # => ["alice"]

  # grouping: ... collects every value for a repeated key into a list
  by_team = { for name, u in local.users : u.team => name... }
  # => { platform = ["alice", "carol"], shop = ["bob"] }
}
```

Over a map, `for k, v in map` gives key and value; over a list, `for i, v in list` gives index and value. Without the grouping `...`, a repeated key in a map `for` is an error ("Duplicate object key").

That's the opening example decoded: `{ for i, az in local.azs : az => cidrsubnet(var.vpc_cidr, 8, i + 10) }` builds a map from AZ (Availability Zone) name to subnet CIDR (Classless Inter-Domain Routing) block, and `for_each` creates one subnet per entry, with `each.key` = the AZ and `each.value` = the CIDR.

### Flattening nested data

A common real shape: "for every environment, for every AZ, one subnet". Nested `for` gives a list of lists; `flatten` makes it one list, and then a `for` turns it into a map keyed by something unique:

```hcl
locals {
  tiers = ["public", "private"]

  subnet_list = flatten([
    for t_i, tier in local.tiers : [
      for a_i, az in local.azs : {
        key  = "${tier}-${az}"
        tier = tier
        az   = az
        cidr = cidrsubnet("10.0.0.0/16", 8, t_i * 10 + a_i)
      }
    ]
  ])

  subnets = { for s in local.subnet_list : s.key => s }
  # => { "public-eu-west-1a" = {...cidr = "10.0.0.0/24"}, ..., "private-eu-west-1a" = {...cidr = "10.0.10.0/24"}, ... }
}
```

### Splat

`[*]` is a short `for` that takes one attribute from every element of a list:

```hcl
aws_instance.web[*].id            # same as [for i in aws_instance.web : i.id]
var.subnets[*].cidr
```

It works on **lists** (resources with `count`). A resource with `for_each` is a **map**, so the splat doesn't apply; use `values()` first, or a `for`:

```hcl
values(aws_subnet.private)[*].id
[for s in aws_subnet.private : s.id]
```

## Stage 6: functions

Terraform has built-in functions only (no user-defined functions in plain HCL). The fastest way to learn them is `terraform console`, an interactive prompt that evaluates expressions (in a folder with a config, it can also read `var.`, `local.` and resources from the state):

```bash
$ terraform console
> cidrsubnet("10.0.0.0/16", 8, 2)
"10.0.2.0/24"
> cidrhost("10.0.2.0/24", 10)
"10.0.2.10"
> merge({a = 1, b = 2}, {b = 3})
{
  "a" = 1
  "b" = 3
}
> [for az in ["a", "b"] : "eu-west-1${az}"]
[
  "eu-west-1a",
  "eu-west-1b",
]
> exit
```

The ones that show up constantly:

| Function | Example | Result |
|---|---|---|
| `length` | `length(["a","b"])` | `2` |
| `lookup` | `lookup({dev="t3.micro"}, "prod", "t3.small")` | `"t3.small"` (default if the key is missing) |
| `merge` | `merge(local.common_tags, {Name = "web"})` | Maps combined, **later wins** |
| `concat` | `concat(["a"], ["b","c"])` | `["a","b","c"]` |
| `flatten` | `flatten([["a"], ["b", ["c"]]])` | `["a","b","c"]` |
| `distinct` | `distinct(["a","a","b"])` | `["a","b"]` |
| `contains` | `contains(["dev","prod"], var.environment)` | `true`/`false` |
| `keys` / `values` | `keys({a=1,b=2})` | `["a","b"]` (sorted) |
| `zipmap` | `zipmap(["a","b"], [1,2])` | `{a=1, b=2}` |
| `toset` / `tolist` / `tomap` | `toset(["b","a","b"])` | `["a","b"]` as a set |
| `one` | `one(aws_eip.web[*].public_ip)` | The single element, or `null` for an empty list (good with `count = 0/1`) |
| `try` | `try(var.config.port, 80)` | First expression that doesn't error |
| `can` | `can(regex("^t3\\.", var.type))` | `true` if it evaluates without error (used in validations) |
| `coalesce` | `coalesce(var.name, local.default_name)` | First non-null, non-empty value |
| `format` | `format("%s-%03d", "web", 7)` | `"web-007"` |
| `join` / `split` | `join(",", ["a","b"])` | `"a,b"` |
| `replace` | `replace("shop_dev", "_", "-")` | `"shop-dev"` |
| `lower` / `upper` / `trimspace` | `lower("Shop")` | `"shop"` |
| `regex` | `regex("^arn:aws:iam::(\\d+)", local.arn)[0]` | The account ID (identifier) captured |
| `cidrsubnet` | `cidrsubnet("10.0.0.0/16", 4, 1)` | `"10.0.16.0/20"` (add 4 bits, take block 1) |
| `cidrhost` | `cidrhost("10.0.1.0/24", 5)` | `"10.0.1.5"` |
| `jsonencode` / `jsondecode` | `jsonencode({Version = "2012-10-17"})` | A JSON (JavaScript Object Notation) string, e.g. for IAM (Identity and Access Management) policies |
| `yamlencode` / `yamldecode` | `yamldecode(file("users.yaml"))` | Data read from YAML (YAML Ain't Markup Language) |
| `file` | `file("${path.module}/script.sh")` | File contents as a string |
| `templatefile` | `templatefile("${path.module}/user_data.sh.tftpl", { env = var.environment })` | A rendered template file |
| `base64encode` | `base64encode(local.script)` | For APIs (application programming interfaces) that want base64 |
| `range` / `setproduct` | `setproduct(["dev","prod"], ["a","b"])` | Every combination |
| `timestamp` | `timestamp()` | The current time. **Changes on every run** (see the traps) |

`jsonencode` beats hand-written JSON for policies: HCL checks the syntax, and I can use references and conditionals inside:

```hcl
resource "aws_s3_bucket_policy" "assets" {
  bucket = aws_s3_bucket.assets.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "DenyInsecureTransport"
      Effect    = "Deny"
      Principal = "*"
      Action    = "s3:*"
      Resource  = [aws_s3_bucket.assets.arn, "${aws_s3_bucket.assets.arn}/*"]
      Condition = { Bool = { "aws:SecureTransport" = "false" } }
    }]
  })
}
```

## Stage 7: dynamic blocks

Arguments take expressions, but **nested blocks** can't be produced by a `for` expression directly. When the number of nested blocks depends on data, `dynamic` generates them:

```hcl
variable "ingress_ports" {
  type    = list(number)
  default = [80, 443]
}

resource "aws_security_group" "legacy" {
  name = "legacy"

  dynamic "ingress" {               # the label = the nested block type to generate
    for_each = var.ingress_ports
    content {                       # the body of each generated block
      from_port   = ingress.value   # the iterator is named after the block: ingress.key / ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}
```

That produces the two `ingress` blocks from Stage 1. `iterator = port` renames `ingress.value` to `port.value` when it's confusing.

> [!tip] Use dynamic blocks sparingly
> They make code harder to read. Prefer a separate resource per item with `for_each` when the provider offers one (for security groups: `aws_vpc_security_group_ingress_rule`). Keep `dynamic` for nested blocks that only exist as blocks.

## Stage 8: comments, files, formatting

```hcl
# single-line comment (the usual style)
// also a single-line comment
/* multi-line
   comment */
```

A folder of `.tf` files is **one** module: Terraform concatenates them. The file names are conventions for humans:

| File | Holds |
|---|---|
| `versions.tf` (or `terraform.tf`) | The `terraform` block: `required_version`, `required_providers`, `backend` |
| `providers.tf` | `provider` blocks |
| `main.tf` | The resources (split into `network.tf`, `compute.tf`… when it grows) |
| `variables.tf` | `variable` blocks |
| `outputs.tf` | `output` blocks |
| `locals.tf` | `locals` (or at the top of `main.tf`) |
| `*.tftpl` | Templates for `templatefile` |
| `*.tfvars` | Variable values, not code |

Terraform also accepts the same language as JSON in `*.tf.json` files, which is useful when another program **generates** Terraform code.

`terraform fmt` rewrites files to the canonical style (two-space indent, aligned `=`). `terraform fmt -recursive -check` in CI (continuous integration) fails the build if anything isn't formatted ([[Terraform testing and validation]]).

```bash
$ terraform fmt -recursive
main.tf
modules/network/variables.tf
```
(It lists the files it changed.)

## Advanced problems

### 1. "Invalid for_each argument ... cannot be determined until apply"
**Symptom:** `The "for_each" map includes keys derived from resource attributes that cannot be determined until apply`.
**Cause:** the **keys** of a `for_each` come from something unknown at plan time, like `for_each = toset(aws_subnet.private[*].id)` on a first apply. Terraform must know how many instances and their addresses during the plan.
**Fix:** key on values known in the code (AZ names, static names), and put unknown values in the map's **values**: `for_each = { for az, s in aws_subnet.private : az => s.id }` uses `az` as the key, which is known.

### 2. Indexing a set
**Symptom:** `Elements of a set are identified only by their value and don't have any separate index or key`.
**Cause:** `toset(...)[0]` or a data source attribute that's a set. Sets have no order.
**Fix:** `tolist(x)[0]`, or `one(x)` when there's exactly one element, or redesign around keys.

### 3. `${` inside a shell script template
**Symptom:** `templatefile` fails with "Invalid reference" on a line like `echo ${HOME}`, or a variable silently disappears.
**Cause:** in templates and strings, `${...}` is Terraform interpolation, so `${HOME}` is read as a Terraform reference.
**Fix:** escape as `$${HOME}` (and `%%{` for a literal `%{`), or use the bare `$HOME` form in shell, which Terraform leaves alone.

### 4. A permanent diff from `timestamp()` or uuid()
**Symptom:** every plan shows `~ tags = { "CreatedAt" = "2026-10-09T10:12:01Z" -> (known after apply) }`.
**Cause:** `timestamp()` and `uuid()` return a new value on every run.
**Fix:** don't use them in arguments. For a stable value, use the `time_static` resource from the `hashicorp/time` provider, or `lifecycle { ignore_changes = [tags["CreatedAt"]] }`.

### 5. Map keys that look like numbers or have dashes
**Symptom:** `{ eu-west-1a = "x" }` errors, or a key `1` doesn't match `"1"`.
**Cause:** an unquoted key must be a valid identifier; and map keys are **always strings**.
**Fix:** quote such keys: `{ "eu-west-1a" = "x" }`. To use a variable's **value** as a key, wrap it in parentheses: `{ (var.key_name) = "x" }`. Without them, a bare key like `key_name` is taken as the literal string `"key_name"`, not as a reference.

## Practice

> [!example]- What does `{ for i, az in ["eu-west-1a", "eu-west-1b"] : az => cidrsubnet("10.0.0.0/16", 8, i) }` produce?
> `{ "eu-west-1a" = "10.0.0.0/24", "eu-west-1b" = "10.0.1.0/24" }`. Curly brackets with `=>` build a map; `i` is the index, `az` the value.

> [!example]- `tags = { … }` vs `ingress { … }`: why is one written with `=` and the other without?
> `tags` is an argument whose value is a map; `ingress` is a nested block. The provider's schema decides which is which. Nested blocks can repeat and can be generated with `dynamic`; arguments appear once and take expressions.

> [!example]- How do I get every instance ID from `aws_instance.web` created with `count`, and from `aws_subnet.private` created with `for_each`?
> `aws_instance.web[*].id` (a list, so the splat works). For the for_each resource (a map): `values(aws_subnet.private)[*].id` or `[for s in aws_subnet.private : s.id]`.

> [!example]- How do I set an argument only in prod and leave the provider default elsewhere?
> `argument = var.environment == "prod" ? "value" : null`. `null` means the argument isn't set.

> [!example]- Group these users by team: `{ alice = "platform", bob = "shop", carol = "platform" }`.
> `{ for name, team in var.users : team => name... }` gives `{ platform = ["alice", "carol"], shop = ["bob"] }`. Without `...` it's a duplicate-key error.

## Easy to get wrong
- `locals { }` block but `local.name` reference (singular)
- Writing `"${var.x}"` when `var.x` is enough
- Using `[*]` on a `for_each` resource: it's a map, use `values()` or a `for`
- Expecting a set to keep order or support `[0]`
- Both branches of `? :` must have compatible types
- `<<EOT` keeps indentation; `<<-EOT` strips it
- `${` in templates is Terraform's: escape shell variables as `$${VAR}`
- Unquoted map keys must be identifiers; to use a variable as a key, wrap it: `(var.k)`
- Thinking file names matter: every `.tf` in the folder is one module
- `timestamp()` and `uuid()` in arguments cause a diff on every plan
- `for_each` keys must be known at plan time

## Related
- Builds on:: [[Terraform]]
- Next step:: [[Terraform variables, locals and outputs]], [[Terraform resources and data sources]]
- Used by:: [[Terraform modules]], [[Terraform providers]], [[Terraform state]]
- Checked by:: [[Terraform testing and validation]] (fmt, validate)
- Area:: [[Infrastructure as code]]

## Flashcards
#flashcards

What is HCL? :: HashiCorp Configuration Language, the language of .tf files: blocks containing arguments whose values are expressions
What are the parts of resource "aws_vpc" "main" { ... }? :: Block type (resource), two labels (resource type and local name), and a body of arguments and nested blocks
Argument vs nested block in HCL? :: An argument is name = value and appears once; a nested block is name { ... } without =, and can repeat
How do you reference a data source attribute? :: data.<type>.<name>.<attribute>, e.g. data.aws_availability_zones.available.names
locals block vs local reference? :: The block is locals { }, the reference is local.<name>
What does null mean as an argument value? :: The argument is unset, so the provider default applies
list vs set vs tuple? :: List: ordered, one element type. Set: unordered, unique, no index. Tuple: ordered, each element can have its own type
map vs object? :: Map: any string keys, one value type. Object: fixed named attributes, each with its own type
What does optional(bool, false) do in an object type? :: Makes the attribute optional, with false as the default
How do you write a literal ${ in a Terraform string? :: $${
<<EOT vs <<-EOT? :: <<- strips the common leading indentation; << keeps the text exactly
What does the ~ do in %{ for x in list ~}? :: Strip marker: removes adjacent whitespace and newlines so loops don't leave blank lines
What decides whether a for expression returns a list or a map? :: The brackets: [for ...] gives a list, {for ... : k => v} gives a map
What does ... do at the end of a map for expression? :: Groups values with the same key into a list instead of failing on duplicate keys
How do you filter in a for expression? :: Add if <condition> at the end: [for n, u in users : n if u.admin]
What does aws_instance.web[*].id do? :: Splat: the id of every element of the list (count resources)
Why doesn't [*] work on a for_each resource? :: A for_each resource is a map, not a list; use values(x)[*].id or a for expression
What is terraform console for? :: An interactive prompt to evaluate expressions and functions, with access to the config's variables and state
cidrsubnet("10.0.0.0/16", 8, 2)? :: "10.0.2.0/24"
What does merge do with duplicate keys? :: The later map wins
try vs can? :: try returns the first expression that doesn't error; can returns true/false whether an expression evaluates without error
Why use jsonencode for IAM policies? :: HCL checks the syntax and you can use references and conditionals inside
What does a dynamic block do? :: Generates repeated nested blocks from a collection; the iterator is named after the block (ingress.value)
Why should dynamic blocks be used sparingly? :: They hurt readability; a separate resource per item with for_each is clearer when the provider offers one
Do .tf file names matter to Terraform? :: No, every .tf file in a folder is read as one module; names are conventions (main.tf, variables.tf, outputs.tf, versions.tf)
What does terraform fmt -check do? :: Fails if any file isn't in canonical format, without changing it (for CI)
Why must for_each keys be known at plan time? :: Terraform needs every instance's address during the plan; unknown values can only go in the map values
Why is timestamp() a bad argument value? :: It changes on every run, so every plan shows a diff
How do you use a variable's value as a map key? :: Wrap it in parentheses: { (var.k) = "x" }
