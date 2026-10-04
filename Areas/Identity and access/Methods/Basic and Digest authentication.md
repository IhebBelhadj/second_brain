---
type: concept
created: 2026-10-04
topic: Identity and access
confidence: 1
tags: [identity, authentication, http, basic-auth, digest-auth]
aliases: [Basic authentication, Basic auth, HTTP Basic, Digest authentication, Digest auth, HTTP Digest, htpasswd]
---
# Basic and Digest authentication

> [!abstract] In one sentence
> **Basic** authentication is HTTP (Hypertext Transfer Protocol)'s built-in scheme where the client sends `username:password`, **base64-encoded (not encrypted)**, in the `Authorization` header of **every** request, so it's only acceptable over TLS (Transport Layer Security); **Digest** was the attempt to avoid sending the password by sending an MD5 (Message Digest 5) hash of it mixed with a server nonce instead, but it forces the server to store password-equivalent hashes, relies on MD5, and became pointless once TLS was everywhere.

## Build-up: protecting the shop's admin page

Staff use `https://admin.shop.example.com/orders` to look at orders. No login exists yet. The fastest possible protection: ask the browser for a username and password.

### Stage 1: the challenge

The server refuses an anonymous request and says which scheme it wants:

```http
GET /orders HTTP/1.1
Host: admin.shop.example.com

HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="shop-admin", charset="UTF-8"
```

The browser sees `WWW-Authenticate: Basic` and shows its **built-in login popup** (no HTML (HyperText Markup Language) form, no JavaScript). The **realm** is a label for the protected area, shown in the popup and used to decide which saved credentials to reuse.

### Stage 2: the answer, base64 of `user:password`

Alice types `alice` / `S3cret!pass`. The browser joins them with a colon, base64-encodes the result, and retries:

```bash
echo -n 'alice:S3cret!pass' | base64
# YWxpY2U6UzNjcmV0IXBhc3M=
```

```http
GET /orders HTTP/1.1
Host: admin.shop.example.com
Authorization: Basic YWxpY2U6UzNjcmV0IXBhc3M=
```

```mermaid
sequenceDiagram
    participant B as Browser
    participant S as admin.shop.example.com
    B->>S: GET /orders
    S-->>B: 401 + WWW-Authenticate: Basic realm="shop-admin"
    Note over B: popup → alice / S3cret!pass
    B->>S: GET /orders + Authorization: Basic YWxpY2U6…
    S->>S: decode, look up alice, verify password hash
    S-->>B: 200 OK
    B->>S: GET /orders/o-8812 + Authorization: Basic YWxpY2U6… (again, automatically)
    S->>S: verify the password AGAIN
    S-->>B: 200 OK
```

> [!warning] Base64 is not encryption
> Anyone who sees the header has the password:
> ```bash
> echo 'YWxpY2U6UzNjcmV0IXBhc3M=' | base64 -d
> # alice:S3cret!pass
> ```
> Base64 only makes arbitrary bytes safe to put in a header. Without HTTPS (Hypertext Transfer Protocol Secure), every request broadcasts the password.

With curl:

```bash
curl -u 'alice:S3cret!pass' https://admin.shop.example.com/orders     # curl builds the header
curl -H 'Authorization: Basic YWxpY2U6UzNjcmV0IXBhc3M=' https://admin.shop.example.com/orders
curl https://alice:S3cret%21pass@admin.shop.example.com/orders       # in the URL: avoid, ends up in history/logs
```

### Stage 3: the server side, nginx in two lines

The classic use: put Basic auth **in front of** an app that has no login, at the reverse proxy (see [[Reverse proxy]]):

```bash
sudo htpasswd -c -B /etc/nginx/.htpasswd alice      # -B = bcrypt hash
cat /etc/nginx/.htpasswd
# alice:$2y$05$Qk3…                                   ← a bcrypt hash, not the password
```

```nginx
location / {
    auth_basic           "shop-admin";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass           http://127.0.0.1:8080;
}
```

The app behind sees requests only after nginx verified the password (nginx passes the `Authorization` header along unless told otherwise; `$remote_user` holds the name).

### Stage 4: the problems show up

| Problem | Why |
|---|---|
| **The password travels on every request** | Every request is a chance to leak it: a TLS-terminating proxy that logs headers, a debug dump, a misconfigured HTTP listener |
| **The password is checked on every request** | With a proper slow hash (bcrypt ~50–100 ms), a page with 30 requests costs seconds of CPU (central processing unit). Servers cache verifications or use weak hashes, both bad |
| **No logout** | The browser keeps sending the cached credentials until it's closed. The usual trick is to force a `401` with wrong credentials |
| **No MFA (multi-factor authentication), no lockout UI (user interface), no "forgot password"** | The browser popup can't show anything else |
| **Ugly, unbrandable popup** | And phishing pages can imitate it |
| **The real password is the credential** | Leaking it compromises everything that password opens, not just this app |

The fix for most of these is to log in **once** and get a temporary credential: [[Session authentication]] for browsers, tokens for APIs (application programming interfaces).

### Stage 5: Digest, an attempt to stop sending the password

Before HTTPS was common, **Digest** (RFC (Request for Comments, an internet standards document) 2617, then 7616) tried to prove knowledge of the password **without sending it**: the server sends a random **nonce**, the client answers with a hash of the password mixed with that nonce.

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Digest realm="shop-admin", qop="auth", nonce="7c1f9a2e4b", opaque="5ccc069c"
```

The client computes, in three steps:

```text
HA1      = MD5(username : realm : password)
HA2      = MD5(method : uri)
response = MD5(HA1 : nonce : nc : cnonce : qop : HA2)
```

- `nc` (nonce count, `00000001`, `00000002`…) and `cnonce` (a client nonce) stop an attacker from replaying the same response
- Only `response` is sent, never the password

Worked out for Alice:

```bash
HA1=$(echo -n 'alice:shop-admin:S3cret!pass' | md5sum | cut -d' ' -f1)   # 0f4792c95c644247071ebbfcfa52be78
HA2=$(echo -n 'GET:/admin/orders' | md5sum | cut -d' ' -f1)               # 7a38315bde603738becc708b10de1b9c
echo -n "$HA1:7c1f9a2e4b:00000001:f3a91c0d:auth:$HA2" | md5sum | cut -d' ' -f1
# f40fb8f027afec8cc52557a57542e448
```

```http
GET /admin/orders HTTP/1.1
Authorization: Digest username="alice", realm="shop-admin", nonce="7c1f9a2e4b",
  uri="/admin/orders", qop=auth, nc=00000001, cnonce="f3a91c0d",
  response="f40fb8f027afec8cc52557a57542e448", opaque="5ccc069c"
```

The server does the same computation and compares. (The RFC's own example, user `Mufasa`, password `Circle Of Life`, gives `6629fae49393a05397450978507c4ef1`: a good test vector.)

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server (stores HA1 per user)
    C->>S: GET /admin/orders
    S-->>C: 401 Digest realm, nonce=7c1f…, qop=auth
    C->>C: HA1 = MD5(alice:shop-admin:password)<br/>response = MD5(HA1:nonce:nc:cnonce:qop:HA2)
    C->>S: Authorization: Digest … response=f40f…
    S->>S: recompute with stored HA1, compare
    S-->>C: 200 OK
```

### Stage 6: why Digest died

| Problem | Explanation |
|---|---|
| **The server must store HA1 (hash 1: MD5 of username:realm:password)** | To recompute the response it needs `MD5(user:realm:password)`. That value is **password-equivalent**: whoever steals it can authenticate without ever knowing the password. It can't be bcrypt or argon2, because the protocol fixes the hash |
| **MD5** | Fast and broken; a leaked HA1 database is cracked quickly. RFC 7616 added SHA-256 (SHA: Secure Hash Algorithm), but browsers barely implemented it |
| **Only partial protection** | Headers and body aren't protected (`qop=auth-int` covered the body, almost never supported). A man in the middle can still read and change everything else |
| **TLS made it pointless** | Once the connection is encrypted, sending the password (Basic) is protected, and the server can store a proper slow hash |
| **Same UX (user experience) problems as Basic** | Popup, no logout, no MFA |

Today Digest survives mostly in **embedded devices** (IP (Internet Protocol) cameras, printers, SIP (Session Initiation Protocol) phones, some routers) and old enterprise gear. New systems: Basic over TLS for the simplest cases, otherwise sessions or tokens.

## Basic vs Digest side by side

| | Basic | Digest |
|---|---|---|
| Sends | `base64(user:password)` | MD5-based response to a server nonce |
| Password on the wire | Yes (encoded) | No |
| Replay protection | None (TLS needed) | Nonce + counter |
| Server stores | Any hash, ideally bcrypt/argon2 | HA1 = MD5(user:realm:password), password-equivalent |
| Needs TLS | Absolutely | Still yes (everything else is visible) |
| Today | Internal tools, simple APIs, machine endpoints over HTTPS | Legacy devices |

## Where Basic is still fine (with HTTPS)

- Internal tools behind a VPN (virtual private network) or SSO (single sign-on) proxy as a second gate
- Machine-to-machine endpoints where the "password" is a long random token: Git over HTTPS uses Basic with a **personal access token** as the password, many registries and Prometheus scrape targets accept it too
- Quick protection for a staging site against crawlers

## Advanced problems

### 1. Credentials leaking through the URL or logs

`https://user:pass@host/` ends up in shell history, CI (continuous integration) logs and proxy logs. Some tools log full request headers at debug level. Use `curl -u` with a variable or a `.netrc` file (`chmod 600`), and scrub `Authorization` in logging.

### 2. The browser keeps logging in after "logout"

The browser caches Basic credentials per realm until the window closes. Workarounds (a request with deliberately wrong credentials to overwrite the cache, a new realm) are hacks. If logout matters, Basic is the wrong tool.

### 3. Basic auth on a CORS API

A browser app calling a Basic-protected API from another origin triggers a **preflight** `OPTIONS` request without credentials. If the server demands auth on `OPTIONS` too, the preflight gets 401 and the real request never happens. Exempt `OPTIONS` from authentication.

### 4. Slow hashes making every request slow

Verifying bcrypt on every request of a busy API costs real CPU. Either cache the result briefly (in memory, keyed by a fast hash of the header) or, better, switch to a token or session issued after one verification.

## In AWS
- ALB (Application Load Balancer) doesn't do Basic auth natively; teams use CloudFront Functions or Lambda@Edge to check a Basic header in front of a staging site, or put the site behind ALB's OIDC (OpenID Connect) authentication instead
- [[Systems Manager]] Parameter Store or Secrets Manager hold the htpasswd content or the credentials for machine clients

## Practice

> [!example]- Decode `Authorization: Basic Ym9iOmh1bnRlcjI=`. What does that say about Basic's security?
> `bob:hunter2`. Base64 is reversible encoding, so Basic is only as safe as the TLS around it.

> [!example]- Why does Digest force the server to store a password-equivalent value?
> To verify, the server recomputes MD5(HA1:nonce:…), so it must store HA1 = MD5(user:realm:password). Anyone holding HA1 can authenticate.

> [!example]- What are nc and cnonce for in Digest?
> A counter and a client nonce so the same response can't be replayed.

> [!example]- Why is Basic auth with a slow password hash a performance problem?
> The password is checked on every request, so every request pays the hash cost.

> [!example]- Git asks for a username and password over HTTPS. What should the password be, and which scheme carries it?
> A personal access token, sent with Basic authentication.

## Easy to get wrong
- Calling base64 "encryption"
- Basic auth over plain HTTP, even "just internally"
- Credentials in URLs (Uniform Resource Locators)
- Thinking Digest makes TLS unnecessary
- Storing Digest HA1 values as if they weren't secrets
- Expecting a working logout with Basic
- Requiring auth on CORS (Cross-Origin Resource Sharing) preflight requests

## Related
- Concepts first:: [[Authentication and authorization]]
- Next step (log in once):: [[Session authentication]], [[JWT and bearer tokens]]
- Replay protection done properly:: [[HMAC request signing]]
- Transport:: [[HTTP]], [[TLS]], [[Reverse proxy]]
- Area:: [[Identity and access]]

## Flashcards
#flashcards

What does a Basic auth header contain? :: Authorization: Basic base64(username:password)
Is Basic auth encrypted? :: No, base64 is reversible encoding; it requires TLS
How does a server ask for Basic auth? :: 401 with WWW-Authenticate (WWW: World Wide Web): Basic realm="…"
What is the realm? :: A label for a protected area, shown in the prompt and used to reuse cached credentials
Why is Basic auth expensive with bcrypt? :: The password is verified on every request
Why is logout hard with Basic auth? :: The browser caches and resends credentials until it closes
How do you set up Basic auth in nginx? :: auth_basic "realm"; auth_basic_user_file with an htpasswd file (bcrypt via htpasswd -B)
Digest HA1? :: MD5(username:realm:password)
Digest HA2 (hash 2: MD5 of method:uri)? :: MD5(method:uri)
Digest response? :: MD5(HA1:nonce:nc:cnonce:qop:HA2)
Why did Digest fail? :: Server stores password-equivalent MD5 hashes, MD5 is weak, little protection beyond the password, TLS made it pointless
Where is Digest still found? :: Embedded devices: cameras, printers, SIP phones
How does Git over HTTPS authenticate? :: Basic auth with a personal access token as the password
Why exempt OPTIONS from Basic auth on a CORS API? :: Preflight requests carry no credentials; a 401 blocks the real request
