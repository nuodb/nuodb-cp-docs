---
title: "Basic Authentication"
description: ""
summary: ""
date: 2024-08-14T13:52:09+03:00
lastmod: 2024-08-14T13:52:09+03:00
draft: false
weight: 220
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

The Control Plane REST API supports authentication with a username/password combination ([HTTP basic authentication](https://tools.ietf.org/html/rfc7617)).
This allows a user to use a fixed username/password combination which will never expire unless the password has changed.

This is the simplest authentication mechanism, but has some security implications if the credentials are exposed to an attacker. To reduce security exposure, consider [Token Authentication]({{< ref "token-authentication.md" >}}) instead.

## Examples

The user name is supplied in the format `<organization>/<user>` along with the password.

{{< tabs "login" >}}
{{< tab "nuodb-cp" >}}

```sh
nuodb-cp httpclient -u acme/dbuser -p "$PASS" ...
```

{{< /tab >}}
{{< tab "curl" >}}

```sh
curl -u "acme/dbuser:$PASS" ...
```

{{< /tab >}}
{{< /tabs >}}

### Bypassing Authentication on local requests

If the REST server property `com.nuodb.controlplane.server.bypassLocalAuthentication` is set to `true`, then authentication and access control can be bypassed by issuing requests from a client on the same host as the REST server.
