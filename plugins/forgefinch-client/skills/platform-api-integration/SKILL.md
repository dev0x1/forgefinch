---
name: platform-api-integration
description: Use when a React, Next.js, or Electron client consumes a separately owned REST, SSE, or OpenAPI backend through typed adapters and generated clients.
---

# Platform API Integration

Read `AGENTS.md` and inspect the client and backend contract locations before
editing. Repository-owned paths, commands, authentication rules, and generated
client tooling are authoritative.

## Use this skill when

- adding or changing REST, SSE, OpenAPI, generated-client, or API adapter work
- deciding whether credentials belong in an Electron main process, a web BFF,
  or a browser-safe client
- mapping transport DTOs into application-owned view models
- testing capability discovery, partial failures, or API compatibility

## Discover the contract first

1. Find the canonical OpenAPI or protocol source and its owning repository.
2. Find generated-client commands and generated output; never edit generated
   files by hand.
3. Confirm the target operation is reachable through the real backend router,
   not merely present in a schema or generated client.
4. Identify authentication, account context, idempotency, correlation, and
   streaming requirements.
5. If the backend checkout or contract is unavailable, report synchronization
   and live verification as blocked rather than recreating the contract.

## Runtime boundaries

### Electron

- Keep tokens, privileged configuration, request signing, and long-lived SSE
  lifecycle in Electron main.
- Expose narrow typed operations through preload; never expose raw transport,
  headers, tokens, or a generic proxy to the renderer.
- Keep the renderer browser-safe and map responses into renderer-owned view
  models before presentation.
- If the application also embeds a local executor, keep local execution and
  canonical backend traffic as separate channels.

### Server-rendered web applications

- Keep credentials and token refresh in server-only modules or a BFF. Give the
  browser only an opaque secure session.
- Use fixed Server Actions or route handlers for browser mutations. Do not
  accept arbitrary operation identifiers, actor identities, or authority
  headers from browser-controlled input.
- Pass validated, minimal view models to Client Components.

### Browser-only clients

- Use authorization flows designed for public clients and never embed secrets.
- Validate untrusted responses at runtime when generated types do not provide
  runtime validation.
- Keep retry, cancellation, cache, and error ownership in one adapter layer.

## Contract and data rules

- Treat the backend contract as the transport source of truth and the owning
  client feature as the presentation source of truth.
- Do not copy DTOs into hand-maintained lookalikes. Generate them or wrap them
  with explicit application models.
- Preserve unavailable and optional values. Do not invent identifiers, counts,
  permissions, lifecycle state, or empty collections for missing fields.
- Keep authentication failures distinct from authorization, not-found,
  dependency-unavailable, validation, malformed-response, and network errors.
- Do not use `404 Not Found` for capability or version discovery. Prefer
  explicit capability and contract-version metadata.
- A valid session must not become signed out merely because an optional
  resource failed.
- Keep fixture adapters test-only and impossible to activate as fallback after
  a production API failure.

## Verification

Use repository-owned commands to cover the affected layers:

- generated-client or contract drift check
- adapter unit tests for mapping, headers, errors, cancellation, and SSE parsing
- component or route tests for loading, partial success, denial, and recovery
- Electron main/preload tests when privileged transport is involved
- one live contract or end-to-end path when the change depends on real routing

Record the backend revision or contract version used, commands that actually
ran, blocked checks, and residual compatibility risk.
