#!/bin/sh

[ -f "$1" ] || (echo "File $1 does not exist" >&2; exit 1)
cat <<EOF | cat - "$1" | sed -e '/^# .*/d' > "$1.tmp" && mv "$1.tmp" "$1"
---
title: "$2"
description: "${3}"
summary: ""
draft: false
weight: ${4:-"900"}
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---
EOF
