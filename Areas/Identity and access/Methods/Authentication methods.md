---
type: subtopic
created: 2026-10-09
topic: Identity and access
tags: [subtopic, identity-and-access]
---
# Authentication methods

> What this covers: authentication and authorization, every authentication method, and choosing between them.

Part of [[Identity and access]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[Authentication and authorization]]: who are you vs what may you do (401 vs 403, broken object-level authorization), the three factors, why stateless HTTP (Hypertext Transfer Protocol) forces every request to carry proof, the two families (send the secret each time vs exchange it for a session/token), stateful vs stateless verification, where credentials travel, storing passwords (argon2id, bcrypt), the map of methods and the threats they face
- [[Basic and Digest authentication]]: the `401` + `WWW-Authenticate` challenge, `base64(user:password)` (decoded by hand: not encryption), nginx `auth_basic` with htpasswd, why it breaks down (password on every request, slow hashes, no logout), Digest's nonce + MD5 (Message Digest 5) response computed step by step, why Digest died (password-equivalent HA1 (hash 1: MD5 of username:realm:password), MD5, TLS (Transport Layer Security)), where Basic is still fine
- [[API keys]]: one key per client, high-entropy keys with prefixes for secret scanning, storing them hashed and showing them once, lookup → rate limit → scope, zero-downtime rotation with two keys, why keys don't belong in browsers or mobile apps, personal access tokens, API (application programming interface) keys vs OAuth client credentials, leaks, API Gateway's usage-plan keys aren't authentication
- [[Session authentication]]: login form → random session ID (identifier) → session store → cookie, cookie flags (`HttpOnly`, `Secure`, `SameSite`, `__Host-`), sharing sessions across servers (sticky vs Redis vs signed cookies), CSRF (Cross-Site Request Forgery) and its defenses, session fixation, idle and absolute timeouts, instant revocation, when cookies get awkward (mobile, cross-origin, BFF (backend for frontend))
- [[JWT and bearer tokens]]: bearer semantics, opaque vs self-contained tokens, a JWT (JSON Web Token; JSON: JavaScript Object Notation) built by hand with openssl, claims (`iss`, `sub`, `aud`, `exp`), verification steps, HS256 (HMAC with Secure Hash Algorithm 256) vs RS256 (Rivest–Shamir–Adleman signature with Secure Hash Algorithm 256) and JWKS (JSON Web Key Set) key rotation, `alg: none` and algorithm confusion, the revocation problem, where JWTs fit and where they don't
- [[Access and refresh tokens]]: the lifetime dilemma, two tokens with two audiences, the refresh flow, rotation and reuse detection (token families), where each client stores tokens (BFF, SPA (single-page application) memory, Keychain/Keystore, CLI (command-line interface)), idle vs absolute lifetimes, `offline_access`, sender-constrained tokens (DPoP (Demonstrating Proof of Possession), mTLS (mutual TLS)), parallel refresh races
- [[HMAC request signing]]: why bearer secrets aren't enough for webhooks, HMAC-SHA256 (SHA256: Secure Hash Algorithm, 256-bit) over the raw body (computed by hand), constant-time comparison, timestamps and nonces against replay, AWS SigV4 (Signature Version 4) (canonical request, string to sign, derived signing key, presigned URLs (Uniform Resource Locators)), HMAC (hash-based message authentication code) vs API keys vs mTLS vs asymmetric signatures
- [[Multi-factor authentication and passkeys]]: factor strength from SMS (Short Message Service) to FIDO2 (Fast IDentity Online 2), TOTP (time-based one-time password) computed step by step (HMAC of the time step, dynamic truncation), MFA fatigue and number matching, WebAuthn (Web Authentication) registration and login, why passkeys are phishing-resistant, synced passkeys vs security keys, rollout and recovery, what MFA doesn't protect (stolen sessions)
- [[Choosing an authentication method]]: every method side by side (what travels, how it's checked, revocation, best use), the three questions that sort them, a decision flowchart, and how the shop combines all of them in one architecture

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
