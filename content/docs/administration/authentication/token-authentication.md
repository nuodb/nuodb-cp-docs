---
title: "Token Authentication"
description: ""
summary: ""
date: 2024-08-14T13:52:09+03:00
lastmod: 2024-08-14T13:52:09+03:00
draft: false
weight: 215
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

Token authentication enhances security by allowing access restrictions and an expiration to be specified when generating the token credentials.
If the token is exposed to an attacker, they would only have limited access to the resources and the token would become invalid after it expires.

The token is secured by a secret key [configured](#securing--encrypting-the-token) on the REST server.

A token can be created by authenticating with a valid `username/password` combination (Basic Authentication) or by authenticating with an existing token against the `/login` resource.
To minimize security risks, the request body should contain appropriate permissions and expiration times.
The server would respond with a `token` which can be used for subsequent calls to the REST services.

For basic authentication requests, the requested permissions cannot exceed the authenticated user.
When logging in via a token, the expiration time and permissions cannot exceed the token used for authentication.

## Token creation (authentication)

A token is created and returned by sending a `POST /login` request and providing user credentials (i.e. username/password).

Here is a simplified example of creating authentication token:

```text
POST /login
Authorization: Basic YnN...
{...}

HTTP/1.1 200 OK
{"token":"eyJ6a..."}
```

## Using the Token to access resources

The value of the `token` attribute returned from the `/login` resource is passed into the `Authorization` header using the `Bearer` authorization scheme.

For example:

```text
GET /users/acme/orgadmin
Authorization: Bearer eyJ6a....

HTTP/1.1 OK
{"organization":"acme","name"......}
```

## Token Expiration

The token expiration can be set with the `expiresIn` or `expiresAtTime` parameter.
If both are specified, `expiresAtTime` takes precedence.
If none are specified, it will set to the default of 2 hours.

- `expiresIn` needs to be a number followed by either "s", "m" or "h" or a combination of them. It will create a token which will expire in the specified number of seconds, minutes or hours from now
- `expiresAtTime` specifies the time when the token should expire. It must be in ISO-8601 format, i.e. `YYYY-MM-DDTHH:MM:SSZ`

{{< callout context="tip" title="Tip" icon="outline/brand-hipchat" >}}
The expiration timestamp should be chosen carefully.
If it is set too far into the future, an exposure of the token to an attacker could give them access to the resource for an extended period of time.
If the expiration is set too small, it would require the user to provide their credentials more often.
{{< /callout >}}

For example, supply `expiresIn` to limit the token expiration:

```text
POST /login
Authorization: Basic YWN.....
{"expiresIn":"3h"}

HTTP/1.1 200 OK
{"token":"eyJ6a...."}
```

For example, use default token expiration settings:

```text
POST /login
Authorization: Basic YWN.....
{"expiresAtTime":"2025-05-22T16:00:00Z"}

HTTP/1.1 200 OK
{"token":"eyJ6a...."}
```

## Authorization (Access Rules)

The user's access rules are controlled by [Access Rule Entries]({{< ref "user-access-rules.md" >}}).

- if `limitAllow` rules are specified in the request, it will replace the existing "allow" rules for the user. If the user requests more permission than they (or the token during re-issue) has, the request will be rejected.
- if a `extraDeny` rule is specified, it will further restrict the user's permissions (it will be added to the user's deny rules, not replaced)
- The response fill return the resulting access levels for the user (a combination of the current user's (or token's) access rules with the requested ones)

For example:

```text
POST /login
Authorization: Basic YWN.....
{"limitAllow":["all:acme","read:corp"],"extraDeny":["delete:acme"]}

HTTP/1.1 200 OK
{"token":"eyJ6a....", "accessRule":{"allow":["all:acme","raed:corp"], "deny":["delete:corp","delete:acme"]}}
```

## Re-Issuing a token

Re-issuing a token with an existing token is permitted, but for security reasons restricted:

- a re-issue of the token cannot exceed the existing expiration time
- specified access rules cannot exceed the existing access rules for the current token

There are several scenarios where re-issuing a token is useful:

- a token with a long expiration (stored in a very secure place like a security vault) can be created which can be used to re-issue a short lived token which could be shared with a temporary job.
- a token with higher permissions (access rules) can be re-issued with less access. For example a background process might need only read permissions.

For example:

```text
POST /login
Authorization: Bearer eyJ6.....
{"limitAllow":["all:acme","read:corp"],"extraDeny":["delete:acme"]}

HTTP/1.1 200 OK
{"token":"abc...."}
```

## Token payload

Once a user performs a login (via POST /login), the response will have a "token" attribute containing a [JWT token](https://datatracker.ietf.org/doc/html/rfc7519). For security reasons this token is encrypted.

## Create and read a token

If the `acme/orgadmin` user doesn't exist yet, [create]({{< ref "user-management.md" >}}#creating-users) it.

{{< tabs "token" >}}
{{< tab "nuodb-cp" >}}

```sh
nuodb-cp httpclient POST login --user acme/orgadmin --password secret \
  -d '{"extraDeny": ["write:*", "delete:*"]}' --jsonpath token --unquote
```

```json
{"token":"eyJ6aXAiOi...","accessRule": {"allow": ["all:acme"], "deny":"extraDeny":["write:*", "delete:*"]},"expiresAtTime":"2024-02-20T17:41:00Z"}
```

The returned token can be used by subsequent `nuodb-cp` commands by either setting the `NUODB_CP_TOKEN` environment variable or passing it to the `--token` argument.

{{< /tab >}}
{{< tab "curl" >}}

Set the environment variable `NUODB_CP_URL_BASE` to the REST service location, e.g. `http://server:8080`

```sh
curl -X POST -H "Content-Type: application/json" $NUODB_CP_URL_BASE/login -u acme/orgadmin:passw0rd \
  -d '{"limitAllow":["all:acme"]}'
```

```json
{"token":"eyJ6aXAiOi...","accessRule": {"allow": ["all:acme"], "deny":"extraDeny":[]},"expiresAtTime":"2024-02-20T17:41:00Z"}
```

Authenticate the user with the token:

```sh
curl $NUODB_CP_URL_BASE/users/acme -H "Authorization: Bearer eyJ6aXAiOi...."
```

```json
{"items":["orgadmin"]}
```

{{< /tab >}}
{{< /tabs >}}

### Re-Issuing tokens with reduced permissions

Especially for short running batch processes, it is often useful, to give a short lived token with minimal permissions to reduce a security exposure.
For example a parent process having a token with a long lived expiration date, can request a short lived token from the server and pass it to a child process to minimize security exposure.

{{< tabs "login" >}}
{{< tab "nuodb-cp" >}}

```sh
export NUODB_CP_TOKEN="$(nuodb-cp httpclient POST login \
  --token "eyJ6aXAi0i..." \
  -d '{"limitAllow": ["read:acme"]}' --jsonpath token --unquote)"
nuodb-cp database list acme
```

{{< /tab >}}
{{< tab "curl" >}}

```sh
curl -X POST -H "Content-Type: application/json" $NUODB_CP_URL_BASE/login -H "Authorization: Bearer eyJ6aXAiOi..." \
  -d '{"limitAllow":["read:acme"]}'
```

```json
{"token":"abc..."}
```

{{< /tab >}}
{{< /tabs >}}

## Appendix

### Securing / Encrypting the token

The token is secured by either a secret key or a cryptographically secure (and strong) password.
A Kubernetes secret will store this information and helm charts will create this key automatically if it doesn't exist.
Changing the key or password will invalidate all active tokens.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: nuodb-cp-runtime-config
  namespace: nuodb
type: Opaque
data:
  secretPassword: .....
```

- secretKey - binary key. If not set, the `secretPassword` needs to be specified.
- secretPassword - password to convert into a key. Ignored if secretKey is specified. Please ensure it has sufficient strength.
- secretKeyAlgorithm - algorithm of the secret key. Defaults to `HmacSHA256` if it is not set.
- secretPasswordToKeyAlgorithm - algorithm to convert a password into a key. Defaults to `PBKDF2WithHmacSHA256` if it is not set.
- secretPasswordToKeyIterations - key generation iterations if `secretPassword` is set. Defaults to `65536` if set to a non-positive value.
- secretPasswordToKeyLength - key length if `secretPassword` is set. Defaults to `256` if set to a non-positive value.

#### Create a secret password key in Kubernetes

```sh
kubectl create secret generic nuodb-cp-runtime-config --from-literal secretPassword=changeIt
```
