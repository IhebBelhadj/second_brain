---
type: topic
created: 2026-10-04
tags: [topic]
---
# Identity and access

> What this covers: how systems know **who** is calling and **what** they may do: authentication methods (passwords, sessions, keys, tokens, signatures, MFA), the protocols that delegate and federate identity (OAuth (Open Authorization) 2.0, OpenID Connect, SAML (Security Assertion Markup Language), SSO), and how to choose between them. Vendor-neutral first. AWS (Amazon Web Services)'s own identity services ([[IAM]], [[AWS Identity Center]], Cognito) live in the AWS area and are linked from here.

## Sub-topics
Each sub-topic has its own index with the same reading order, for studying one part at a time (and a cleaner graph).
- [[Identity and access › Methods]]: authentication and authorization, every authentication method, and choosing between them
- [[Identity and access › Protocols]]: delegation and federation: OAuth 2.0, OpenID Connect, single sign-on

## How to use this

Read the sections **top to bottom**: each one assumes the ones above it. Links in *italics* are notes I haven't written yet (the roadmap).

```mermaid
flowchart TD
    F["1. Foundations<br/>authN vs authZ, factors, stateless HTTP"] --> M1["2. Sending a secret<br/>Basic/Digest, API keys"]
    M1 --> M2["3. Log in once, then a credential<br/>sessions, JWT, access + refresh"]
    M2 --> M3["4. Proofs instead of secrets<br/>HMAC signing, MFA, passkeys"]
    M3 --> P["5. Delegation and federation<br/>OAuth 2.0, OIDC, SSO"]
    P --> C["6. Choosing<br/>which method where"]
```

## 1. Foundations
- [[Authentication and authorization]]: who are you vs what may you do (401 vs 403, broken object-level authorization), the three factors, why stateless HTTP (Hypertext Transfer Protocol) forces every request to carry proof, the two families (send the secret each time vs exchange it for a session/token), stateful vs stateless verification, where credentials travel, storing passwords (argon2id, bcrypt), the map of methods and the threats they face

## 2. Sending a secret with every request
- [[Basic and Digest authentication]]: the `401` + `WWW-Authenticate` challenge, `base64(user:password)` (decoded by hand: not encryption), nginx `auth_basic` with htpasswd, why it breaks down (password on every request, slow hashes, no logout), Digest's nonce + MD5 (Message Digest 5) response computed step by step, why Digest died (password-equivalent HA1 (hash 1: MD5 of username:realm:password), MD5, TLS (Transport Layer Security)), where Basic is still fine
- [[API keys]]: one key per client, high-entropy keys with prefixes for secret scanning, storing them hashed and showing them once, lookup → rate limit → scope, zero-downtime rotation with two keys, why keys don't belong in browsers or mobile apps, personal access tokens, API (application programming interface) keys vs OAuth client credentials, leaks, API Gateway's usage-plan keys aren't authentication

## 3. Log in once, then carry a credential
- [[Session authentication]]: login form → random session ID (identifier) → session store → cookie, cookie flags (`HttpOnly`, `Secure`, `SameSite`, `__Host-`), sharing sessions across servers (sticky vs Redis vs signed cookies), CSRF (Cross-Site Request Forgery) and its defenses, session fixation, idle and absolute timeouts, instant revocation, when cookies get awkward (mobile, cross-origin, BFF (backend for frontend))
- [[JWT and bearer tokens]]: bearer semantics, opaque vs self-contained tokens, a JWT (JSON Web Token; JSON: JavaScript Object Notation) built by hand with openssl, claims (`iss`, `sub`, `aud`, `exp`), verification steps, HS256 (HMAC with Secure Hash Algorithm 256) vs RS256 (Rivest–Shamir–Adleman signature with Secure Hash Algorithm 256) and JWKS (JSON Web Key Set) key rotation, `alg: none` and algorithm confusion, the revocation problem, where JWTs fit and where they don't
- [[Access and refresh tokens]]: the lifetime dilemma, two tokens with two audiences, the refresh flow, rotation and reuse detection (token families), where each client stores tokens (BFF, SPA (single-page application) memory, Keychain/Keystore, CLI (command-line interface)), idle vs absolute lifetimes, `offline_access`, sender-constrained tokens (DPoP (Demonstrating Proof of Possession), mTLS (mutual TLS)), parallel refresh races

## 4. Proofs instead of secrets
- [[HMAC request signing]]: why bearer secrets aren't enough for webhooks, HMAC-SHA256 (SHA256: Secure Hash Algorithm, 256-bit) over the raw body (computed by hand), constant-time comparison, timestamps and nonces against replay, AWS SigV4 (Signature Version 4) (canonical request, string to sign, derived signing key, presigned URLs (Uniform Resource Locators)), HMAC (hash-based message authentication code) vs API keys vs mTLS vs asymmetric signatures
- [[Multi-factor authentication and passkeys]]: factor strength from SMS (Short Message Service) to FIDO2 (Fast IDentity Online 2), TOTP (time-based one-time password) computed step by step (HMAC of the time step, dynamic truncation), MFA fatigue and number matching, WebAuthn (Web Authentication) registration and login, why passkeys are phishing-resistant, synced passkeys vs security keys, rollout and recovery, what MFA doesn't protect (stolen sessions)
- Also in Networking: [[mTLS]] (client certificates), [[Workload identity (SPIFFE)]] (service identities without secrets)

## 5. Delegation and federation
- [[OAuth 2.0]]: the password anti-pattern, the four roles, the authorization code flow parameter by parameter, why a code and not a token, PKCE (Proof Key for Code Exchange) for public clients, scopes and consent, client credentials for machines, the device code flow (`aws sso login`, `gh auth login`), deprecated grants and OAuth 2.1, why OAuth isn't login, redirect URI (Uniform Resource Identifier) attacks and consent phishing
- [[OpenID Connect]]: what OAuth was missing for login, the ID token vs the access token, validating an ID token (`aud`, `nonce`), identifying users by `iss` + `sub` (not email), discovery and JWKS, scopes/claims/UserInfo, logout (RP-initiated (RP: relying party), back-channel), OIDC for machines (GitHub Actions, Kubernetes), OIDC vs SAML
- [[Single sign-on]]: one IdP (identity provider) for many apps, why the second login is silent (the IdP session), SAML's AuthnRequest/assertion/ACS (ACS: Assertion Consumer Service) flow with a real assertion, SAML vs OIDC, SP-initiated (SP: service provider) vs IdP-initiated, JIT (just-in-time) vs SCIM (System for Cross-domain Identity Management) provisioning and leavers, the risks of one basket (availability, compromise, break-glass accounts)
- Not written yet: *[[SAML]]* (deep dive: bindings, metadata, signature wrapping) · *[[Kerberos]]* (tickets, KDC (Key Distribution Center), Windows domains) · *[[LDAP and Active Directory]]* (directories, binds, groups)

## 6. Choosing
- [[Choosing an authentication method]]: every method side by side (what travels, how it's checked, revocation, best use), the three questions that sort them, a decision flowchart, and how the shop combines all of them in one architecture
- Not written yet: *[[Authorization models]]* (RBAC (role-based access control), ABAC (attribute-based access control), ReBAC (relationship-based access control), policy engines like OPA (Open Policy Agent) and Cedar)

## Related areas
- [[Networking]]: [[HTTP]] (stateless requests, headers), [[TLS]] and [[mTLS]], [[Certificates and PKI]], [[Encryption basics]] (signatures, HMAC, key pairs), [[Reverse proxy]] (auth at the edge)
- [[AWS]]: the AWS reading path is [[AWS security]]. [[IAM]] (SigV4, policies), [[STS]] (roles, trust policies, temporary credentials), [[AWS Identity Center]] (workforce SSO), [[Connecting GitHub Actions to AWS]] and [[ECS production stack]] (GitHub OIDC to AWS), Cognito

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE topic = this.file.name AND confidence
SORT confidence ASC
```

## Open questions
- 
