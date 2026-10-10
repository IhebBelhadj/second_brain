---
type: concept
created: 2026-10-04
topic: Identity and access
subtopic: Authentication methods
confidence: 1
tags: [identity, authentication, jwt, tokens, bearer, cryptography]
aliases: [JWT, JSON Web Token, Bearer token, Bearer tokens, Bearer authentication, JWS, JWE, JWKS, Opaque token, Token introspection, Claims]
---
# JWT and bearer tokens

> [!abstract] In one sentence
> A **bearer token** is a credential that works for **whoever holds it** (like cash), sent as `Authorization: Bearer <token>`; a **JWT** is one popular format for such a token: three base64url parts, `header.payload.signature`, where the payload carries **claims** about the caller (who, issued by whom, for which API (application programming interface), until when) and the signature lets any server **verify it without a database lookup**, which is why JWTs scale so well and why they're so hard to revoke before they expire.

## Build-up: the shop splits into services

The shop's backend became several services: `orders`, `catalog`, `payments`, behind an API gateway. A central login service `auth.shop.example.com` authenticates users. With [[Session authentication]], every service would have to call the session store (or the auth service) **on every request** to learn who the caller is.

### Stage 1: the bearer idea

Whatever the format, the client gets a **token** after login and sends it on each request:

```http
GET /v1/orders HTTP/1.1
Host: api.shop.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3Mi…
```

"Bearer" (RFC (Request for Comments, an internet standards document) 6750) means: **possession is proof**. No password, no key ownership to demonstrate, the token itself is enough. Consequences:
- Anyone who copies it (logs, XSS (cross-site scripting), a compromised proxy) **is** the user until it expires
- So: TLS (Transport Layer Security) always, short lifetimes, never in URLs (Uniform Resource Locators), careful storage

Two kinds of bearer tokens:

| | **Opaque** token | **Self-contained** token (JWT) |
|---|---|---|
| Looks like | `8f2c6a91d4e07b35…` (random) | `eyJhbGci…` (encoded JSON (JavaScript Object Notation) + signature) |
| Means | Nothing by itself: a reference | Carries the identity and permissions |
| Service checks it by | Asking the issuer (**introspection**) or a shared store | Verifying the **signature** locally |
| Revoke now | Yes (delete it) | Not without extra machinery |
| Like | A session ID (identifier) in a header | A signed letter of introduction |

### Stage 2: anatomy of a JWT

A JWT is `base64url(header) . base64url(payload) . base64url(signature)`. Building one by hand shows there's no magic:

```bash
b64url() { openssl base64 -A | tr '+/' '-_' | tr -d '='; }

H=$(printf '%s' '{"alg":"HS256","typ":"JWT"}' | b64url)
P=$(printf '%s' '{"iss":"https://auth.shop.example.com","sub":"user-4821","aud":"api.shop.example.com","scope":"orders:read","iat":1791100800,"exp":1791101700}' | b64url)
S=$(printf '%s' "$H.$P" | openssl dgst -sha256 -hmac 'dev-only-secret' -binary | b64url)
echo "$H.$P.$S"
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGguc2hvcC5leGFtcGxlLmNvbSIsInN1YiI6InVzZXItNDgyMSIsImF1ZCI6ImFwaS5zaG9wLmV4YW1wbGUuY29tIiwic2NvcGUiOiJvcmRlcnM6cmVhZCIsImlhdCI6MTc5MTEwMDgwMCwiZXhwIjoxNzkxMTAxNzAwfQ.Pn5dF1D_ywezPhYML-Pyy4J4uspRLRu3cT0VuhfkCd4
```

```mermaid
flowchart LR
    subgraph T["the token"]
        H["eyJhbGci…<br/>HEADER"] --- P["eyJpc3Mi…<br/>PAYLOAD"] --- S["Pn5dF1D_…<br/>SIGNATURE"]
    end
    H --> HJ["{ alg: HS256, typ: JWT }<br/>how it's signed"]
    P --> PJ["{ iss, sub, aud,<br/>scope, iat, exp }<br/>the claims"]
    S --> SJ["HMAC-SHA256(<br/>header + '.' + payload,<br/>secret)"]

    classDef h fill:#fdedec,stroke:#c0392b,color:#000
    classDef p fill:#e8f1fb,stroke:#2e86c1,color:#000
    classDef s fill:#eafaf1,stroke:#1e8449,color:#000
    class H,HJ h
    class P,PJ p
    class S,SJ s
```

Anyone can decode the payload, **no key needed**:

```bash
echo "$P" | tr '_-' '/+' | base64 -d 2>/dev/null; echo     # base64url → base64 (padding may need adding)
# {"iss":"https://auth.shop.example.com","sub":"user-4821","aud":"api.shop.example.com","scope":"orders:read","iat":1791100800,"exp":1791101700}
```

> [!warning] Signed, not encrypted
> A JWT (technically a **JWS (JSON Web Signature)**, a signed JWT) is **readable by anyone** who has it: the browser, a log file, a proxy. Never put secrets or personal data you wouldn't show the user in it. The signature only guarantees it **wasn't changed** and **who issued it**. Encrypted JWTs exist (**JWE (JSON Web Encryption)**, five parts) but are rare.

The standard (registered) claims:

| Claim | Meaning | Example |
|---|---|---|
| `iss` | Issuer: who created and signed it | `https://auth.shop.example.com` |
| `sub` | Subject: who it's about (stable user/client ID) | `user-4821` |
| `aud` | Audience: which API it's meant for | `api.shop.example.com` |
| `exp` | Expiry (Unix seconds) | `1791101700` = 08:15 UTC (Coordinated Universal Time) |
| `nbf` | Not valid before | |
| `iat` | Issued at | `1791100800` = 08:00 UTC |
| `jti` | Unique token ID (for denylists, replay detection) | `a1b2c3` |

Plus custom ones: `scope`, `roles`, `tenant`, `email`… The payload is sent on **every request**, so keep it small (headers over ~8 KB (kilobytes) get rejected by proxies and load balancers).

### Stage 3: verifying without a database

The `orders` service receives the token and, without calling anyone:

1. Splits it in three, decodes the header
2. **Recomputes the signature** over `header.payload` with the key, compares with the third part
3. Checks the claims: `exp` in the future, `nbf` in the past, `iss` is my auth server, `aud` is **me**, required scope present
4. Uses `sub` as the identity, then does its own **authorization** (is o-8812 user-4821's order?)

```mermaid
flowchart TB
    T["Bearer token"] --> D["decode header:<br/>alg, kid"]
    D --> A{"alg in my allow-list?<br/>(never 'none', never<br/>what the token says blindly)"}
    A -- no --> R["401"]
    A -- yes --> K["pick key by kid<br/>(cached JWKS)"]
    K --> V{"signature valid?"}
    V -- no --> R
    V -- yes --> C{"exp, nbf, iss,<br/>aud = me, scope?"}
    C -- no --> R
    C -- yes --> ID["identity = sub<br/>→ app authorization"]

    classDef bad fill:#fdedec,stroke:#c0392b,color:#000
    classDef ok fill:#eafaf1,stroke:#1e8449,color:#000
    class R bad
    class ID ok
```

In practice a library does this (`PyJWT`, `jose`, `jsonwebtoken`, gateway plugins), **configured** with the expected algorithms, issuer and audience:

```python
import jwt
claims = jwt.decode(token, key, algorithms=["RS256"],
                    issuer="https://auth.shop.example.com",
                    audience="api.shop.example.com")
```

### Stage 4: whose key? (HS256 vs RS256 and JWKS)

With **HS256 (HMAC with Secure Hash Algorithm 256)** (HMAC (hash-based message authentication code)), the **same secret** signs and verifies. Every service that verifies tokens could also **mint** them: a leak from the least protected service lets an attacker forge tokens for all of them.

With **asymmetric** algorithms (**RS256 (Rivest–Shamir–Adleman signature with Secure Hash Algorithm 256)** RSA (Rivest–Shamir–Adleman), **ES256 (Elliptic Curve Digital Signature Algorithm with Secure Hash Algorithm 256)** ECDSA (Elliptic Curve Digital Signature Algorithm), EdDSA (Edwards-curve Digital Signature Algorithm)), the auth server signs with a **private key** it never shares; services verify with the **public key**, which can be published openly:

| | HS256 | RS256 / ES256 |
|---|---|---|
| Keys | One shared secret | Private (sign) + public (verify) |
| Who can mint tokens | Everyone holding the secret | Only the issuer |
| Distribution | Secret copied to every verifier | Public key published at a URL |
| Use | One service issuing and verifying its own tokens | Any multi-service or third-party setup |

The public keys are published as a **JWKS** (JSON Web Key Set) at a well-known URL:

```bash
curl -s https://auth.shop.example.com/.well-known/jwks.json | jq '.keys[] | {kid, kty, alg, use}'
# { "kid": "2026-09", "kty": "RSA", "alg": "RS256", "use": "sig" }
# { "kid": "2026-10", "kty": "RSA", "alg": "RS256", "use": "sig" }
```

The token header names its key: `{"alg":"RS256","kid":"2026-10"}`. Verifiers cache the JWKS and refetch when they meet an unknown `kid`. **Key rotation** then needs no coordination:

```mermaid
sequenceDiagram
    participant AS as Auth server
    participant J as JWKS endpoint
    participant API as orders service
    AS->>J: publish new key 2026-10 (old 2026-09 still listed)
    Note over AS: wait > JWKS cache time
    AS->>AS: start signing with kid 2026-10
    API->>API: token with unknown kid → refetch JWKS → verify ✓
    Note over AS: wait > max token lifetime
    AS->>J: remove 2026-09
```

### Stage 5: the attacks on careless verification

| Attack | How it works | Defense |
|---|---|---|
| **`alg: none`** | Attacker sends `{"alg":"none"}` with no signature; a naive library accepts it | Allow-list algorithms in the verifier; reject `none` |
| **Algorithm confusion** | Server expects RS256; attacker sends `alg: HS256` signed with the server's **public key** used as an HMAC secret. A library that picks the algorithm from the token verifies it "successfully" | Fix the algorithm per key on the server side, never trust the header's `alg` |
| **Missing `aud` check** | A token issued for `catalog` (or for another customer's app on the same IdP) is accepted by `payments` | Always check `aud` |
| **Missing `exp` check** | Expired tokens keep working | Libraries do it by default; don't disable it |
| **`kid` / `jku` injection** | The header points to an attacker's key URL or a file path | Only use keys from the configured JWKS URL |
| **Weak HS256 secret** | `secret123` is brute-forced offline from any captured token | 256-bit random secrets, or asymmetric keys |
| **Decode instead of verify** | Code reads `sub` with a decode-only function | Grep for `verify=False`, `decode(` without key |

### Stage 6: the price of statelessness (revocation)

Alice clicks "log out", or an admin disables a compromised account. With sessions, deleting the record ends it. A JWT is checked **only by signature and expiry**: every service keeps accepting it until `exp`.

Options, from simplest:

| Approach | How | Cost |
|---|---|---|
| **Short lifetimes** | Access tokens live 5–15 minutes; a [[Access and refresh tokens\|refresh token]] (stateful, revocable) gets new ones | Revocation takes effect within minutes, not instantly |
| Denylist | Store revoked `jti`s (or "tokens for user X issued before T") until they'd expire; services check it | A lookup per request again, but a small, short-lived set |
| Introspection | Services ask the issuer about each token (or cache answers briefly) | Back to a central dependency |
| Key rotation | Rotate the signing key to kill **every** token | Emergency only |

Short-lived access tokens + revocable refresh tokens is the standard answer.

### Stage 7: where JWTs fit, and where they don't

| Good fit | Poor fit |
|---|---|
| Many services or third parties verifying identity without a central lookup | A single web app with server-side sessions already working |
| OAuth (Open Authorization) access tokens, [[OpenID Connect]] ID tokens | Long-lived "remember me" credentials (can't revoke) |
| Short-lived, signed assertions between systems (e.g. GitHub Actions → AWS (Amazon Web Services)) | Storing session state that changes (cart, preferences) |
| Edge or gateway verification | Anything needing instant logout without extra infrastructure |

A common mistake is replacing a perfectly good session cookie with a JWT in `localStorage` "because it's stateless": JavaScript-readable storage turns any XSS into token theft, and logout stops working.

## Advanced problems

### 1. Valid tokens rejected right after issuance (clock skew)

The issuing server's clock is ahead: `iat`/`nbf` are "in the future" for the verifier. Keep NTP (Network Time Protocol) everywhere, allow a small leeway (30–60 s) in verifiers.

### 2. 431 / 400 "Request header too large"

Tokens stuffed with roles, groups and permissions grow past proxy limits (nginx's default `large_client_header_buffers` 8 KB, ALB (Application Load Balancer) limits). Keep tokens lean: put group membership behind an API, or use opaque tokens with introspection.

### 3. Signature fails after the IdP rotated keys

The verifier cached the JWKS forever or pinned a single key. Cache with a TTL (time to live) and refetch on unknown `kid`.

### 4. A token for one app works on another

Two apps registered on the same identity provider, neither checking `aud`. Tokens from app A (maybe a harmless public app) are replayed against app B. Always validate audience.

## In AWS
- **API Gateway HTTP (Hypertext Transfer Protocol) APIs** have a native **JWT authorizer** (issuer + audience + JWKS), ALB can authenticate with OIDC, and **Cognito** issues JWT access and ID tokens
- AWS STS (Security Token Service) itself uses opaque, signed session tokens; but `AssumeRoleWithWebIdentity` **accepts** JWTs from OIDC providers (GitHub Actions, EKS (Elastic Kubernetes Service) service accounts), verifying them against the provider's JWKS (see [[ECS production stack#Stage 0: the pipeline needs state and a way to log in]])

## Practice

> [!example]- Can anyone read a JWT's claims? Can anyone change them?
> Read: yes, it's only base64url. Change: no, the signature would no longer verify.

> [!example]- Why prefer RS256 over HS256 when ten services verify tokens?
> With HS256 every verifier holds the secret and could mint tokens. With RS256 only the issuer holds the private key; verifiers use the public key.

> [!example]- What is the algorithm confusion attack?
> The server expects RS256 but trusts the token's alg header; the attacker signs with HS256 using the public key as the secret, and the library accepts it.

> [!example]- How does a service find the right public key for a token?
> The header's `kid` names a key in the issuer's JWKS, which the service caches.

> [!example]- A user is disabled but keeps working for 10 minutes. Why, and is that acceptable?
> Their JWT access token is valid until exp. Acceptable if access tokens are short and refresh tokens are revoked; otherwise add a denylist.

> [!example]- Opaque token vs JWT for an API used only by one backend?
> Opaque tokens with a lookup (or introspection) are simpler to revoke; JWTs pay off when many verifiers can't easily reach a central store.

## Easy to get wrong
- Treating JWT payloads as private
- Trusting the token's `alg` header
- Not checking `aud` (and `iss`)
- Decoding without verifying
- HS256 with a weak or widely shared secret
- Long-lived JWTs with no revocation story
- JWTs in `localStorage`
- Huge tokens in headers
- No clock leeway, or no NTP

## Related
- Concepts first:: [[Authentication and authorization]]
- The stateful alternative:: [[Session authentication]]
- Lifetimes and renewal:: [[Access and refresh tokens]]
- Where JWTs come from:: [[OAuth 2.0]], [[OpenID Connect]]
- Signatures underneath:: [[Encryption basics]], [[HMAC request signing]]
- Area:: [[Identity and access]]

## Flashcards
#flashcards

What is a bearer token? :: A credential that grants access to whoever holds it, sent as Authorization: Bearer
Opaque token vs JWT? :: Opaque: random reference checked by lookup/introspection. JWT: self-contained claims verified by signature
Three parts of a JWT? :: base64url header . payload . signature
Is a JWT encrypted? :: No (JWS is signed only); anyone can read the payload. JWE is the encrypted form
What do iss, sub, aud, exp mean? :: Issuer, subject (who), audience (which API), expiry
What must a verifier check on a JWT? :: Allowed alg, signature with the right key, exp/nbf, iss, aud, required scopes
HS256 vs RS256? :: HS256: shared secret signs and verifies. RS256: private key signs, public key verifies
What is a JWKS? :: A JSON set of public keys published by the issuer, selected by kid
How does key rotation work with JWKS? :: Publish new key, wait for caches, sign with it, remove old key after max token lifetime
What is the alg none attack? :: An unsigned token with alg none accepted by a naive verifier
What is algorithm confusion? :: An RS256 public key used as an HS256 secret by an attacker, accepted if the server trusts the alg header
Why is revoking JWTs hard? :: They're verified by signature and expiry alone, without a lookup
Standard answer to JWT revocation? :: Short-lived access tokens plus revocable refresh tokens (denylist if needed)
What is token introspection? :: Asking the issuer whether a token is active and what it contains
Why keep JWT payloads small? :: They're sent on every request; large headers hit proxy limits
