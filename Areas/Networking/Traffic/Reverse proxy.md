---
type: concept
created: 2026-09-27
topic: Networking
confidence: 1
tags: [networking, proxy, http, web]
aliases: [Reverse proxies, X-Forwarded-For, PROXY protocol, TLS termination, API gateway]
---
# Reverse proxy

> [!abstract] In one sentence
> A **reverse proxy** sits in front of servers and receives every request **for them**: clients think it *is* the server. Because it ends the client's connection and opens its own to a backend, it's the natural place to terminate TLS, route requests, balance load, cache, compress, rate-limit and authenticate, once, instead of in every application. Load balancers, API gateways, CDNs, ingress controllers and service mesh sidecars are all reverse proxies with a different focus.

## Why it exists: building it up

### Problem 1: one public IP, many apps
I have one server with a public IP and three apps: a website, an API and an admin panel, each on its own port internally. Users should just use `https://example.com`, `https://api.example.com`. Only one program can listen on port 443.

**Fix:** one program listens on 443 and **routes by host name and path** to the right app:

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;
    ssl_certificate     /etc/ssl/api.crt;
    ssl_certificate_key /etc/ssl/api.key;

    location / {
        proxy_pass http://127.0.0.1:8080;                     # the API
        proxy_set_header Host              $host;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Problem 2: every app handles TLS, badly
Each app has its own certificate config, its own TLS settings, its own renewal. **Fix: TLS termination at the proxy.** One place for certificates, protocols and ciphers ([[TLS]], [[Certificate rotation]]), and the apps behind speak plain HTTP (or re-encrypted TLS if the network behind isn't trusted, see [[mTLS]]).

### Problem 3: one server isn't enough
The app needs three copies. **Fix:** the proxy sends requests to a **pool** of backends and skips dead ones: that's a load balancer (see [[Load balancing]]).

### Problem 4: every app re-implements the same cross-cutting stuff
Rate limiting, authentication, compression, caching static files, security headers, request size limits, blocking bad requests (WAF rules). **Fix:** do it once in the proxy. Taken further, this is an **API gateway**.

## What a reverse proxy does

| Job | What it means |
|---|---|
| **Routing** | By host (`api.` vs `www.`), path (`/api/*`), header, method, cookie |
| **TLS termination** | Decrypts at the edge, one place for certificates. Can also *originate* TLS to backends (re-encryption) |
| **Load balancing** | Spreads requests across backends, health checks (see [[Load balancing]]) |
| **Caching** | Serves repeated responses without hitting the app (respects `Cache-Control`) |
| **Compression** | gzip/brotli once at the edge |
| **Protection** | Rate limiting, request size limits, WAF rules, hiding backend details and versions |
| **Authentication** | Checks a session, JWT or client certificate before the request reaches the app (OAuth2 proxy pattern) |
| **Protocol translation** | HTTP/2 or HTTP/3 to clients, HTTP/1.1 to old backends. WebSockets and gRPC passthrough |
| **Buffering** | Absorbs slow clients so the app's workers aren't held by someone on a bad 3G link |

## The problem every reverse proxy creates: "who is the real client?"

Behind a proxy, the backend's TCP connection comes from **the proxy's IP**, not the client's. Logs, rate limits, geo rules and fraud checks all break: every request seems to come from `10.0.1.5`.

### Fix 1: headers (L7 proxies)

| Header | Carries |
|---|---|
| `X-Forwarded-For` | The client IP chain: `client, proxy1, proxy2` (each proxy **appends** the address it received the connection from) |
| `X-Forwarded-Proto` | `https` if the client used HTTPS (the backend only sees HTTP from the proxy, so apps building redirect URLs need this) |
| `X-Forwarded-Host` | The original `Host` |
| `Forwarded` | The standardized version of all three (RFC 7239): `for=203.0.113.7;proto=https;host=example.com` |

> [!warning] X-Forwarded-For can be forged
> Any client can send `X-Forwarded-For: 1.2.3.4` itself. The proxy appends to it, so the backend sees `1.2.3.4, <real client>`. If the app trusts the **leftmost** value, any attacker can pick their IP (bypassing IP allowlists and rate limits). Rule: trust only entries added by **my own** proxies, i.e. read from the **right**, skipping the known proxy addresses (nginx `set_real_ip_from` + `real_ip_recursive on`). And the backend should only accept connections **from** the proxy, or the header means nothing.

A classic related bug: an app behind a TLS-terminating proxy sees plain HTTP, so it builds `http://` redirect URLs or refuses to set secure cookies → redirect loops. Fix: trust `X-Forwarded-Proto` from the proxy.

### Fix 2: PROXY protocol (L4 proxies)
A TCP load balancer can't add HTTP headers (it doesn't parse HTTP, and the payload may be TLS). The **PROXY protocol** (from HAProxy) prepends a small header at the **start of the TCP connection** with the original client IP and port. The backend must be configured to expect it, otherwise it sees garbage at the start of every connection and all requests fail. Both sides must agree.

### Fix 3: don't hide it at all
Some L4 load balancers **preserve the client source IP** (no source NAT). Then the backend's replies must go back **through** the load balancer, or they'll go directly to the client, who drops them (asymmetric routing). That's why it only works in specific setups (the LB is the backend's gateway, or direct server return, see [[Load balancing]]).

## Other things that break behind a reverse proxy

| Symptom | Cause | Fix |
|---|---|---|
| `502 Bad Gateway` | The proxy couldn't talk to the backend: down, wrong port, connection refused, TLS mismatch to the backend | Check the backend directly from the proxy host |
| `504 Gateway Timeout` | The backend was too slow for the proxy's timeout | Raise the timeout for that route, or make the work asynchronous |
| Random `502`s under load, backend looks healthy | **Keep-alive race**: the backend closes an idle connection at the same moment the proxy reuses it | Backend's keep-alive timeout **longer** than the proxy's idle timeout |
| WebSockets connect then drop | Upgrade headers not forwarded, or idle timeout too short | Forward `Upgrade`/`Connection`, raise idle timeout, send pings |
| Uploads fail above N MB | Proxy body size limit (nginx `client_max_body_size` default 1 MB) | Raise it on that route |
| Wrong links / redirects to `http://` or to the internal hostname | App builds URLs from what it sees | Forward `Host` and `X-Forwarded-Proto`, configure the app's public URL |
| Users see each other's pages | Caching a personalized response | Only cache what's explicitly cacheable, vary on cookies/auth |

## The family: same idea, different focus

| | Focus | Examples |
|---|---|---|
| **Web server as reverse proxy** | Routing + TLS + static files for a few apps | nginx, Caddy, Apache httpd |
| **Load balancer** | Spreading load, health checks, high throughput | HAProxy, nginx, Envoy, hardware appliances, cloud LBs |
| **API gateway** | APIs: auth (keys, OAuth/JWT), per-client quotas, request transformation, versioning, developer portal | Kong, Tyk, Envoy-based gateways, cloud API gateways |
| **CDN** | Many reverse proxies worldwide, close to users, caching and absorbing attacks | Cloudflare, Akamai, Fastly, cloud CDNs |
| **Ingress controller** | Reverse proxy configured by Kubernetes objects (Ingress, Gateway API) | ingress-nginx, Traefik, Envoy Gateway |
| **Sidecar / service mesh proxy** | A reverse *and* forward proxy next to every service, for service-to-service traffic | Envoy in Istio, linkerd2-proxy (see [[Service mesh]]) |

A real request often crosses several: CDN → cloud load balancer → ingress controller → sidecar → app. Each hop adds its own timeouts, headers, size limits and logs, so when something breaks, find **which hop** returned the error first (the `Server` or `Via` header, and each layer's logs).

## Easy to get wrong
- Trusting the leftmost `X-Forwarded-For` value, or trusting it from anyone
- Letting clients reach the backends directly, bypassing the proxy (and its auth, WAF, rate limits)
- Enabling PROXY protocol on one side only
- Backend keep-alive timeout shorter than the proxy's idle timeout (random 502s)
- Default body size and timeouts that are fine for pages but not for uploads, exports and WebSockets
- Caching responses that depend on who's asking

## Related
- The other direction:: [[Proxies]]
- The protocol it speaks:: [[HTTP]], [[HTTP2]] (keep-alive timeouts, HTTP/2 to clients vs HTTP/1.1 to backends), [[WebSocket]] (Upgrade headers)
- What it enables:: [[Load balancing]], [[Service discovery]], [[Service mesh]]
- Security:: [[TLS]], [[mTLS]], [[Certificates and PKI]], [[AWS WAF]]
- Applied:: [[Proxies, load balancing and discovery in AWS]], [[Load balancers]]

## Flashcards
#flashcards

What is a reverse proxy? :: A proxy in front of servers that receives requests for them, clients think it's the server
Four things a reverse proxy centralizes? :: TLS termination, routing by host/path, load balancing, protections (rate limit, auth, WAF), caching/compression
Why do backends behind a proxy see the wrong client IP? :: The TCP connection comes from the proxy
X-Forwarded-For vs PROXY protocol? :: XFF: an HTTP header added by L7 proxies. PROXY protocol: a header at the start of the TCP connection for L4 proxies
How can X-Forwarded-For be abused? :: Clients can send a fake one. Trusting the leftmost value lets them pick their IP
How to read X-Forwarded-For safely? :: From the right, skipping only my own proxies' addresses, and only accept connections from the proxy
What happens if only one side enables PROXY protocol? :: The backend sees an unexpected header (or misses it), and every connection fails
Why do apps behind TLS-terminating proxies build http:// redirects? :: They see plain HTTP from the proxy. Trust X-Forwarded-Proto
502 vs 504 at a reverse proxy? :: 502: couldn't get a valid response from the backend. 504: the backend was too slow for the timeout
Cause of random 502s under load with healthy backends? :: Backend closes idle keep-alive connections while the proxy reuses them. Backend keep-alive must be longer than the proxy's
What is an API gateway? :: A reverse proxy specialized for APIs: auth, quotas, transformation, versioning
What is a CDN in proxy terms? :: A worldwide fleet of caching reverse proxies close to users
