#!/usr/bin/env python3

"""
Generates sample custom resources (CRs) from custom Kubernetes resource definitions (CRDs).
"""

import argparse
import os
import sys
import yaml
import re
import traceback

template = """---
title: "{kind}"
description: "A sample {kind} object with fields documented"
summary: ""
draft: false
weight: {weight}
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## Minimal example

```yaml
{minimal}
```

## Extended example

```yaml
{extended}
```
"""

def find_crd_files(source_dir):
    crd_files = []
    for root, _, files in os.walk(source_dir):
        for f in files:
            if f.endswith((".yaml", ".yml")):
                path = os.path.join(root, f)
                with open(path) as fd:
                    content = fd.read()
                    if "CustomResourceDefinition" in content:
                        crd_files.append(path)
    return crd_files

def resolve_type(schema):
    """
    Resolve the type(s) of a schema node.
    Returns a list of types if `anyOf`, `oneOf`, or `allOf` is present.
    """
    if not schema:
        return ["object"]  # default type

    # Direct type declaration
    if 'type' in schema:
        return [schema['type']]

    types = []

    # anyOf
    if 'anyOf' in schema:
        for subschema in schema['anyOf']:
            types.extend(resolve_type(subschema))
        return types

    # oneOf
    if 'oneOf' in schema:
        for subschema in schema['oneOf']:
            types.extend(resolve_type(subschema))
        return types

    # allOf: merge all types (deduplicated)
    if 'allOf' in schema:
        for subschema in schema['allOf']:
            types.extend(resolve_type(subschema))
        return list(dict.fromkeys(types))  # remove duplicates while preserving order

    # Fallback
    return ["object"]

# Known special patterns (verbatim)
SIZE_PATTERN = r'^(\+|-)?(([0-9]+(\.[0-9]*)?)|(\.[0-9]+))(([KMGTPE]i)|[numkMGTPE]|([eE](\+|-)?(([0-9]+(\.[0-9]*)?)|(\.[0-9]+))))?$'
DURATION_PATTERN = r'^([0-9]+(\.[0-9]+)?(ns|us|µs|ms|s|m|h))+$'

def value_for_schema(schema, field_name=None, parent_field_name=None):
    # Use default if available
    if 'default' in schema:
        return schema['default']

    # Use enum first
    if 'enum' in schema and schema['enum']:
        return schema['enum'][0]

    # Determine based on reference field name
    ref_prefix = None
    if parent_field_name and parent_field_name.endswith("Ref"):
        ref_prefix = parent_field_name[:-3].lower() or "example"
    if ref_prefix is not None and field_name == 'name':
        return f"{ref_prefix}"

    t = resolve_type(schema)
    fmt = schema.get('format', '')
    pattern = schema.get('pattern', None)

    if 'string' in t:
        # Determine based on current field name
        if field_name is not None:
            if field_name == 'version':
                return "7.0.2"
            if field_name == 'dbName':
                return "demo"
            if field_name == 'sla':
                return "prod"
            if field_name == 'namespace':
                return "default"

		# Handle known special patterns first
        if pattern == SIZE_PATTERN:
            return "5Gi"
        if pattern == DURATION_PATTERN:
            return "1d"

        # Handle format
        if fmt == 'date':
            return '2025-11-11'
        if fmt == 'date-time':
            return "2025-11-11T21:30:40.971508Z"
        if fmt == 'email':
            return "example@example.com"
        if fmt == 'uri':
            return "https://example.com"
        if fmt == 'hostname':
            return "example-host"
        if fmt == 'byte':
            return "ZXhhbXBsZQ=="  # base64 for "example"
        if fmt == 'binary':
            return "<binary-data>"

        # Default string fallback
        return "string"

    if 'boolean' in t:
        return 'true'
    if 'integer' in t:
        fmt = schema.get('format', '')
        if fmt in ('int32', 'int64'):
            return 1
        return 1
    if 'number' in t:
        fmt = schema.get('format', '')
        if fmt in ('float', 'double'):
            return 1.00
        return 1.0
    if 'array' in t:
        return []
    if 'object' in t:
        return {}
    return "value"

def match_cel(schema, pattern):
    if cel := schema.get('x-kubernetes-validations', []):
        for exp in cel:
            if match := re.search(pattern, exp['message']):
                return match

# Include any fields that are optional but must be generated in a minimal CR
REQUIRED_FIELDS = {
    'DatabaseBackup' : ['spec.source.databaseRef'],
    'CanaryRolloutTemplate' : ['spec.steps', 'spec.steps.promoteTo'],
    'DatabaseQuota' : ['spec.hard'],
    'HelmFeature' : ['spec.values'],
    'Metric' : ['spec.metrics'],
    'ServiceTier' : ['spec.features'],
    'PersistentVolumeRebinding': [
        'spec.rebindings.template',
        'spec.rebindings.template.sourceClaim.dbaasDatabaseArchive',
        'spec.rebindings.template.targetClaim.dbaasDatabaseArchive'
    ],
}

def write_schema(schema, kind=None, indent=2, minimal=False, field_name=None, field_path=None):
    lines = []
    indent_str = ' ' * indent
    if not schema or 'properties' not in schema:
        return lines
    required_fields = set(schema.get('required', [])) if minimal else None
    required_paths = REQUIRED_FIELDS.get(kind, [])

    for k in sorted(schema['properties']):
        if minimal:
            # Determine if special CEL validation contraints are applied
            if match := match_cel(schema, r"Exactly one of '([^']*)'.*"):
                # Make the first field from a set of mutually exclusive fields
                # required
                required_fields.add(match.group(1))
            # Determine if the field is explicitly required
            if f'{field_path}.{k}' in required_paths:
                required_fields.add(k)
            if k not in required_fields:
                # Skip this field
                continue
        prop = schema['properties'][k]
        if 'description' in prop:
            for desc_line in prop['description'].splitlines():
                lines.append(f"{indent_str}# {desc_line.strip()}")

        t = resolve_type(prop)
        next_field_path = f'{field_path}.{k}' if field_path else k
        val = value_for_schema(prop, field_name=k, parent_field_name=field_name)
        if 'object' in t:
            lines.append(f"{indent_str}{k}:")
            nlines = len(lines)
            if 'properties' in prop and prop['properties']:
                lines.extend(write_schema(
                    prop, kind=kind, indent=indent+2, minimal=minimal,
                    field_name=k, field_path=next_field_path))
            if nlines == len(lines):
                lines.append(f"{indent_str}  {val}")
        elif 'array' in t:
            lines.append(f"{indent_str}{k}:")
            item = prop.get('items', {})
            item_type = resolve_type(item)
            nlines = len(lines)
            if 'object' in item_type:
                lines.append(f"{indent_str}-")
                lines.extend(write_schema(
                    item, kind=kind, indent=indent+2, minimal=minimal, field_name=k, field_path=next_field_path))
            else:
                lines.append(f"{indent_str}- {value_for_schema(item, field_name=k, parent_field_name=field_name)}")
            if nlines == len(lines):
                lines.append(f"{indent_str}{val}")
        else:
            lines.append(f"{indent_str}{k}: {val}")
    return lines

def generate_cr_sample(crd, include_status=False, minimal=False):
    if 'spec' not in crd or 'versions' not in crd['spec'] or not crd['spec']['versions']:
        raise ValueError("CRD missing spec or versions")
    # Support only one version for now
    version_name = crd['spec']['versions'][0]['name']
    version_schema = crd['spec']['versions'][0]['schema'].get('openAPIV3Schema', {})
    group = crd['spec']['group']
    kind = crd['spec']['names']['kind']

    lines = []
    lines.append("# Standard Kubernetes API Version declaration.")
    lines.append(f"apiVersion: {group}/{version_name}")
    lines.append("# Standard Kubernetes Kind declaration.")
    lines.append(f"kind: {kind}")
    lines.append("# Standard Kubernetes metadata.")
    lines.append("metadata:")
    lines.append("  # Sample name. May be any valid Kubernetes object name.")
    lines.append(f"  name: sample-{kind.lower()}")
    lines.append("  # Namespace where the resource will be created.")
    lines.append("  namespace: default")

    spec_schema = version_schema.get('properties', {}).get('spec')
    if spec_schema:
        lines.append(f"# Specification of the desired behavior of the {kind}.")
        lines.append("spec:")
        lines.extend(write_schema(
            spec_schema, kind=kind, indent=2, minimal=minimal,
            field_name='spec', field_path='spec'))

    if include_status:
        status_schema = version_schema.get('properties', {}).get('status')
        if status_schema:
            lines.append(f"# Current observed status of the {kind}.")
            lines.append("status:")
            lines.extend(write_schema(
                status_schema, kind=kind, indent=2, minimal=minimal,
                field_name='status', field_path='spec'))

    return "\n".join(lines)

def main():
    args = parse_args()
    crd_files = find_crd_files(args.source_dir)
    if not crd_files:
        print(f"No CRD files found in {args.source_dir}", file=sys.stderr)
        sys.exit(1)
    os.makedirs(args.output_dir, exist_ok=True)
    print(f"Found {len(crd_files)} CRD(s). Generating samples into {args.output_dir}...")
    weight = int(args.start_weight)
    crd_files.sort()
    for crd_file in crd_files:
        with open(crd_file) as fd:
            crd = yaml.safe_load(fd)
        try:
            sample_yaml = generate_cr_sample(crd, include_status=False, minimal=True)
            extended_sample_yaml = generate_cr_sample(crd, include_status=True, minimal=False)
        except Exception as e:
            print(f"Failed generating sample for {crd_file}: {e}", file=sys.stderr)
            print(traceback.format_exc())
            continue
        kind = crd['spec']['names']['kind']
        group = crd['spec']['group']
        out_file = os.path.join(args.output_dir, f"{group}_{kind.lower()}.md")
        with open(out_file, 'w') as fd:
            fd.write(template.format(
                kind=kind, minimal=sample_yaml, extended=extended_sample_yaml, weight=weight))
        print(f"Generated {out_file}")
        weight += 1

    print("All samples generated successfully.")

def parse_args():
    parser = argparse.ArgumentParser(description="Generate Kubernetes CR samples from CRD YAMLs.")
    parser.add_argument("--source-dir", required=True, help="Directory containing CRD YAML files")
    parser.add_argument("--output-dir", default=".", help="Directory to write generated CR samples")
    parser.add_argument("--start-weight", default=100, help="Starting page weight")
    return parser.parse_args()

if __name__ == "__main__":
    main()
