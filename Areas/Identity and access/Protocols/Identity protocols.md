---
type: subtopic
created: 2026-10-09
topic: Identity and access
tags: [subtopic, identity-and-access]
---
# Identity protocols

> What this covers: delegation and federation: OAuth 2.0, OpenID Connect, single sign-on.

Part of [[Identity and access]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- [[OAuth 2.0]]: the password anti-pattern, the four roles, the authorization code flow parameter by parameter, why a code and not a token, PKCE (Proof Key for Code Exchange) for public clients, scopes and consent, client credentials for machines, the device code flow (`aws sso login`, `gh auth login`), deprecated grants and OAuth 2.1, why OAuth isn't login, redirect URI (Uniform Resource Identifier) attacks and consent phishing
- [[OpenID Connect]]: what OAuth was missing for login, the ID token vs the access token, validating an ID token (`aud`, `nonce`), identifying users by `iss` + `sub` (not email), discovery and JWKS, scopes/claims/UserInfo, logout (RP-initiated (RP: relying party), back-channel), OIDC for machines (GitHub Actions, Kubernetes), OIDC vs SAML
- [[Single sign-on]]: one IdP (identity provider) for many apps, why the second login is silent (the IdP session), SAML's AuthnRequest/assertion/ACS (ACS: Assertion Consumer Service) flow with a real assertion, SAML vs OIDC, SP-initiated (SP: service provider) vs IdP-initiated, JIT (just-in-time) vs SCIM (System for Cross-domain Identity Management) provisioning and leavers, the risks of one basket (availability, compromise, break-glass accounts)

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
