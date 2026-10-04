# Area guide: Identity and access

**Index:** `Identity and access.md` is the learning path (6 numbered sections, each assumes the ones above) with a one-line summary of every note and the planned notes as italic links. Read it for *what* a note covers; use this file for *where* it is.

**Scope:** vendor-neutral identity for a systems engineer: authentication methods (passwords, sessions, API keys, tokens, signatures, MFA), delegation and federation protocols (OAuth 2.0, OIDC, SAML, SSO, Kerberos, LDAP), authorization models. Transport security (TLS, mTLS, PKI, workload identity) stays in `Areas/Networking/Security/` and is linked from the index. AWS identity services (IAM, Identity Center, Cognito) live in `Areas/AWS/Security/` with `topic: AWS`. Notes share one scenario: the shop (`shop.example.com`, `api.shop.example.com`, `auth.shop.example.com`), a mobile app, partners, staff tools.

## Folder map

```
Identity and access/
├── Identity and access.md         topic index (the learning path)
├── Choosing an authentication method.md   (compare) all methods side by side, decision flowchart, the shop's combined architecture
├── Foundations/
│   └── Authentication and authorization.md   authN vs authZ, 401/403, factors, stateless HTTP, stateful vs stateless, carriers, password storage, map, threats
├── Methods/
│   ├── Basic and Digest authentication.md   challenge, base64, nginx htpasswd, limits, Digest computation, why it died
│   ├── API keys.md                one key per client, prefixes, hashed storage, scopes/rate limits, rotation, where not to use, vs client credentials
│   ├── Session authentication.md  session IDs, store, cookie flags, scaling, CSRF, fixation, timeouts, BFF
│   ├── JWT and bearer tokens.md   bearer, opaque vs JWT, anatomy by hand, verification, HS256/RS256/JWKS, attacks, revocation
│   ├── Access and refresh tokens.md   lifetimes, refresh flow, rotation/reuse detection, storage per client, DPoP, races
│   ├── HMAC request signing.md    webhooks, raw-body HMAC, replay windows, AWS SigV4, presigned URLs, comparison
│   └── Multi-factor authentication and passkeys.md   factor strength, TOTP by hand, push fatigue, WebAuthn, passkeys, rollout, limits
└── Protocols/
    ├── OAuth 2.0.md               roles, authorization code step by step, PKCE, scopes, client credentials, device code, deprecated grants, not login
    ├── OpenID Connect.md          ID token vs access token, validation, iss+sub, discovery, claims, logout, machine OIDC, vs SAML
    └── Single sign-on.md          IdP/SP, the IdP session, SAML flow and assertion, provisioning (JIT/SCIM), risks, break-glass
```

## Where a new note goes

| It's about… | Folder |
|---|---|
| Concepts shared by everything (authN/authZ, identity, factors) | `Foundations/` |
| A way a client proves itself (WebAuthn deep dive, client certificates for users, magic links) | `Methods/` |
| A delegation/federation protocol or directory (SAML, Kerberos, LDAP, SCIM) | `Protocols/` |
| Authorization models (RBAC, ABAC, policy engines) | `Foundations/`, or an `Authorization/` folder once 2+ notes share it |
| Comparisons across sections | Area root |
| TLS, mTLS, PKI, SPIFFE | `Areas/Networking/Security/` (link from section 4 of the index) |
| An AWS identity service (IAM, Identity Center, Cognito, Verified Permissions) | `Areas/AWS/Security/`, `topic: AWS`, linked from the index |

The planned notes (roadmap) are the italic `*[[…]]*` links in `Identity and access.md`: when writing one, use that exact name so existing links resolve.
