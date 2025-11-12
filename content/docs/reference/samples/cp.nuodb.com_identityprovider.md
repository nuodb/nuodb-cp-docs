---
title: "IdentityProvider"
description: "A sample IdentityProvider object with fields documented"
summary: ""
draft: false
weight: 959
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## Minimal example

```yaml
# Standard Kubernetes API Version declaration.
apiVersion: cp.nuodb.com/v1beta1
# Standard Kubernetes Kind declaration.
kind: IdentityProvider
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-identityprovider
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the IdentityProvider.
spec:
  # Rules for resolving the user to provision in the NuoDB Control Plane
  # bound to the user authenticated by the external provider. If the user
  # with the resolved organization and name does not exist, then one will
  # be created with the resolved roles and access rule the first time it
  # is authenticated by the REST server.
  provisionUser:
    # Resolver for the user name.
    name:
    # Resolver for the organization the user belongs to.
    organization:
```

## Extended example

```yaml
# Standard Kubernetes API Version declaration.
apiVersion: cp.nuodb.com/v1beta1
# Standard Kubernetes Kind declaration.
kind: IdentityProvider
# Standard Kubernetes metadata.
metadata:
  # Sample name. May be any valid Kubernetes object name.
  name: sample-identityprovider
  # Namespace where the resource will be created.
  namespace: default
# Specification of the desired behavior of the IdentityProvider.
spec:
  # Specification for the Central Authentication Service (CAS) provider.
  cas:
    # The URL of the CAS server.
    serverUrl: string
    # If specified, the endpoint to use to validate service tickets. If
    # omitted, then the `/serviceValidate` endpoint on the server URL is
    # used to validate service tickets according to the CAS protocol
    # specification.
    validateEndpoint:
      # The URL of the endpoint to use to validate service tickets.
      url: string
  # Specification for the OpenID Connect (OIDC) provider.
  oidc:
    # The client ID to use for the OIDC provider.
    clientId:
      # If specified, the Secret resource reference to the value.
      secretRef:
        # The key of the value within the Secret resource.
        key: string
        # The name of the Secret resource to obtain the value from.
        name: secret
      # If specified, the value to use.
      value: string
    # The Secret resource reference to the client secret to use for the
    # OIDC provider.
    clientSecret:
      # The key of the value within the Secret resource.
      key: string
      # The name of the Secret resource to obtain the value from.
      name: string
    # The URL of the OIDC provider.
    issuerUrl: string
    # Whether to disable TLS verification of the server certificate.
    tlsSkipVerify: true
    # The interval at which the OIDC provider configuration is updated via
    # OpenID Connect discovery.
    updateInterval: string
  # Rules for resolving the user to provision in the NuoDB Control Plane
  # bound to the user authenticated by the external provider. If the user
  # with the resolved organization and name does not exist, then one will
  # be created with the resolved roles and access rule the first time it
  # is authenticated by the REST server.
  provisionUser:
    # Resolver for the access rule of the user.
    accessRule:
      # If specified, the JSONPath expression to use to resolve the value
      # from the user attributes in the external provider, which are assumed
      # to be in JSON format.
      jsonPath: string
      # If specified, the value to use.
      value: string
    # Resolver for the user name.
    name:
      # If specified, the JSONPath expression to use to resolve the value
      # from the user attributes in the external provider, which are assumed
      # to be in JSON format.
      jsonPath: string
      # Transformations to apply to the value resolved by evaluating
      # `jsonPath` or to each element of the resolved array of values. If the
      # resolved value is not a value node (e.g. string, number) or an array
      # of value nodes, then `transform` is ignored.
      transform:
      -
        # The value to transform. If `regex` is `true`, this is interpreted as
        # a regular expression that is matched against the input value.
        # Otherwise, this is interpreted as a literal string that is compared
        # fully to the input value. If the `from` value does not match the
        # input value, then this transformation has no effect.
        from: string
        # Whether to apply transformation to all matches of the regular
        # expression. If `global` is `true`, this transformation will be
        # applied to all occurrences of `from` within the current value. If
        # `global` is `false` or omitted, this transformation will be applied
        # to the first occurrence only.
        global: true
        # Whether to interpret `from` as a regular expression.
        regex: true
        # The strategy to use when chaining transformations.
        # 
        # - `Compose` indicates that the output value of the current transformation
        # should be applied as the input value to the next transformation.
        # - `ShortCircuit` indicates that all subsequent transformations should be
        # skipped if the current transformation matched on the input value.
        # 
        # If omitted, the default strategy is based on the `regex` value, with
        # `Compose` being used when `regex` is `true` and `ShortCircuit` being used
        # when `regex` is `false` or omitted.
        strategy: Compose
        # The value to transform to. If `regex` is `true`, this may contain
        # references to capturing groups appearing in the `from` value,
        # otherwise it is just the literal output value.
        to: string
      # If specified, the value to use.
      value: string
    # Resolver for the organization the user belongs to.
    organization:
      # If specified, the JSONPath expression to use to resolve the value
      # from the user attributes in the external provider, which are assumed
      # to be in JSON format.
      jsonPath: string
      # Transformations to apply to the value resolved by evaluating
      # `jsonPath` or to each element of the resolved array of values. If the
      # resolved value is not a value node (e.g. string, number) or an array
      # of value nodes, then `transform` is ignored.
      transform:
      -
        # The value to transform. If `regex` is `true`, this is interpreted as
        # a regular expression that is matched against the input value.
        # Otherwise, this is interpreted as a literal string that is compared
        # fully to the input value. If the `from` value does not match the
        # input value, then this transformation has no effect.
        from: string
        # Whether to apply transformation to all matches of the regular
        # expression. If `global` is `true`, this transformation will be
        # applied to all occurrences of `from` within the current value. If
        # `global` is `false` or omitted, this transformation will be applied
        # to the first occurrence only.
        global: true
        # Whether to interpret `from` as a regular expression.
        regex: true
        # The strategy to use when chaining transformations.
        # 
        # - `Compose` indicates that the output value of the current transformation
        # should be applied as the input value to the next transformation.
        # - `ShortCircuit` indicates that all subsequent transformations should be
        # skipped if the current transformation matched on the input value.
        # 
        # If omitted, the default strategy is based on the `regex` value, with
        # `Compose` being used when `regex` is `true` and `ShortCircuit` being used
        # when `regex` is `false` or omitted.
        strategy: Compose
        # The value to transform to. If `regex` is `true`, this may contain
        # references to capturing groups appearing in the `from` value,
        # otherwise it is just the literal output value.
        to: string
      # If specified, the value to use.
      value: string
    # Resolvers for roles assigned to the user, which are aggregated to
    # obtain the full list of roles assigned to the user.
    roles:
    -
      # If specified, the JSONPath expression to use to resolve the value
      # from the user attributes in the external provider, which are assumed
      # to be in JSON format.
      jsonPath: string
      # Transformations to apply to the value resolved by evaluating
      # `jsonPath` or to each element of the resolved array of values. If the
      # resolved value is not a value node (e.g. string, number) or an array
      # of value nodes, then `transform` is ignored.
      transform:
      -
        # The value to transform. If `regex` is `true`, this is interpreted as
        # a regular expression that is matched against the input value.
        # Otherwise, this is interpreted as a literal string that is compared
        # fully to the input value. If the `from` value does not match the
        # input value, then this transformation has no effect.
        from: string
        # Whether to apply transformation to all matches of the regular
        # expression. If `global` is `true`, this transformation will be
        # applied to all occurrences of `from` within the current value. If
        # `global` is `false` or omitted, this transformation will be applied
        # to the first occurrence only.
        global: true
        # Whether to interpret `from` as a regular expression.
        regex: true
        # The strategy to use when chaining transformations.
        # 
        # - `Compose` indicates that the output value of the current transformation
        # should be applied as the input value to the next transformation.
        # - `ShortCircuit` indicates that all subsequent transformations should be
        # skipped if the current transformation matched on the input value.
        # 
        # If omitted, the default strategy is based on the `regex` value, with
        # `Compose` being used when `regex` is `true` and `ShortCircuit` being used
        # when `regex` is `false` or omitted.
        strategy: Compose
        # The value to transform to. If `regex` is `true`, this may contain
        # references to capturing groups appearing in the `from` value,
        # otherwise it is just the literal output value.
        to: string
      # If specified, the value to use.
      value: string
    # Validations to apply to the user attributes from the external provider.
    validate:
    -
      # If present, the set of values that the resolved value is constrained to.
      enum:
      - string
      # If present, the constraints to apply on all elements of the resolved
      # value, which must be an array of value nodes.
      items:
        # If present, the set of values that the resolved value is constrained to.
        enum:
        - string
        # If present, the regular expression that the resolved value must match.
        pattern: string
      # The JSONPath expression to use to resolve the value from the user
      # attributes in the external provider, which are assumed to be in JSON
      # format.
      jsonPath: string
      # If present, the regular expression that the resolved value must match.
      pattern: string
      # Whether the resolved value is required.
      required: True
      # Transformations to apply to the value resolved by evaluating
      # `jsonPath` or to each element of the resolved array of values. If the
      # resolved value is not a value node (e.g. string, number) or an array
      # of value nodes, then `transform` is ignored.
      transform:
      -
        # The value to transform. If `regex` is `true`, this is interpreted as
        # a regular expression that is matched against the input value.
        # Otherwise, this is interpreted as a literal string that is compared
        # fully to the input value. If the `from` value does not match the
        # input value, then this transformation has no effect.
        from: string
        # Whether to apply transformation to all matches of the regular
        # expression. If `global` is `true`, this transformation will be
        # applied to all occurrences of `from` within the current value. If
        # `global` is `false` or omitted, this transformation will be applied
        # to the first occurrence only.
        global: true
        # Whether to interpret `from` as a regular expression.
        regex: true
        # The strategy to use when chaining transformations.
        # 
        # - `Compose` indicates that the output value of the current transformation
        # should be applied as the input value to the next transformation.
        # - `ShortCircuit` indicates that all subsequent transformations should be
        # skipped if the current transformation matched on the input value.
        # 
        # If omitted, the default strategy is based on the `regex` value, with
        # `Compose` being used when `regex` is `true` and `ShortCircuit` being used
        # when `regex` is `false` or omitted.
        strategy: Compose
        # The value to transform to. If `regex` is `true`, this may contain
        # references to capturing groups appearing in the `from` value,
        # otherwise it is just the literal output value.
        to: string
# Current observed status of the IdentityProvider.
status:
  # The OIDC configuration, which is obtained using OpenID Connect discovery.
  oidc:
    # The `authorization_endpoint` property of OIDC configuration.
    authorizationEndpoint: string
    # The content returned by the OpenID Connect discovery endpoint, which
    # is `<issuerUrl>/.well-known/openid-configuration`.
    configuration: string
    # The error that occurred while obtaining OIDC configuration.
    error: string
    # The number of consecutive attempts to obtain OIDC configuration that
    # have failed.
    errorCount: 1
    # The URL of the OIDC provider.
    issuerUrl: string
    # The content returned by the JSON Web Key Set (JWKS) endpoint
    # appearing in the `jwks_uri` property of OIDC configuration.
    jwks: string
    # The last update time for the OIDC configuration.
    lastUpdateTime: 2025-11-11T21:30:40.971508Z
    # The time that the next update will be scheduled for the OIDC
    # configuration.
    nextUpdateTime: 2025-11-11T21:30:40.971508Z
    # The `token_endpoint` property of OIDC configuration.
    tokenEndpoint: string
```
