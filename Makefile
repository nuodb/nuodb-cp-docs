# Base directory for all cloned Git repositories
GIT_BASE = tmp/repos

# Get the currently used golang install path (in GOPATH/bin, unless GOBIN is set)
ifeq (,$(shell go env GOBIN))
GOBIN=$(shell go env GOPATH)/bin
else
GOBIN=$(shell go env GOBIN)
endif

# Define the project directory
PROJECT_DIR := $(shell pwd)
DOCS_DIR := $(PROJECT_DIR)/content/docs

# NuoDB CP release packages
CP_VERSION ?= 2.9.2
CP_CLIDOC := nuodb-cp.adoc
CP_CLIDOC_FILE := https://github.com/nuodb/nuodb-cp-releases/releases/download/v$(CP_VERSION)/$(CP_CLIDOC)
CP_CRD_CHART := https://github.com/nuodb/nuodb-cp-releases/releases/download/v$(CP_VERSION)/nuodb-cp-crd-$(CP_VERSION).tgz

# NuoDB Control Plane Git repository and revision
CP_REPO ?= github.com/nuodb/nuodb-control-plane
CP_REPO_DIR := $(GIT_BASE)/$(CP_REPO)
CP_COMMIT ?= v$(CP_VERSION)

# Tools used by various targets
CRD_DOCS = bin/crd-ref-docs

# Tool Versions
CRD_DOCS_VERSION ?= 0.2.0

##@ General

# The help target prints out all targets with their descriptions organized
# beneath their categories. The categories are represented by '##@' and the
# target descriptions by '##'. The awk commands is responsible for reading the
# entire set of makefiles included in this invocation, looking for lines of the
# file as xyz: ## something, and then pretty-format the target and help. Then,
# if there's a line with ##@ something, that gets pretty-printed as a category.
# More info on the usage of ANSI control characters for terminal formatting:
# https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_parameters
# More info on the awk command:
# http://linuxcommand.org/lc3_adv_awk.php

.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development

.PHONY: run
run: # Starts a development server
	npm run dev

.PHONY: generate-all
generate-all: generate-cli-docs generate-crd-docs

.PHONY: generate-cli-docs
generate-cli-docs: # Generates reference pages for nuodb-cp CLI tool
	mkdir -p $(PROJECT_DIR)/tmp
	curl -sL $(CP_CLIDOC_FILE) -o $(DOCS_DIR)/reference/$(CP_CLIDOC) \
		&& hack/add_frontmatter.sh $(DOCS_DIR)/reference/$(CP_CLIDOC) \
			"nuodb-cp CLI Reference" \
			"Command-line interface for the NuoDB Control Plane REST Service" "911"

.PHONY: generate-crd-docs
generate-crd-docs: $(CRD_DOCS) $(CP_REPO_DIR) # Generates CRDs reference pages
	cd $(CP_REPO_DIR) && git fetch --all && git checkout $(CP_COMMIT) && cd - \
		&& $(CRD_DOCS) --source-path=$(CP_REPO_DIR)/operator/api/v1beta1 \
			--config=.crdrefdocs.yaml \
			--renderer=markdown \
			--output-mode=group \
			--output-path $(DOCS_DIR)/reference \
		&& hack/add_frontmatter.sh $(DOCS_DIR)/reference/cp.nuodb.com.md \
			"NuoDB CRDs Reference" \
			"Custom resource definitions (CRDs) for NuoDB Control Plane operator" "912"

# Targets for downloading tools used by other targets
ifeq ($(shell uname -m), $(filter $(shell uname -m), arm64 aarch64))
CRD_DOCS_ARCH := arm64
else
CRD_DOCS_ARCH := $(shell uname -m)
endif
$(CRD_DOCS):
	mkdir -p $(PROJECT_DIR)/tmp $(PROJECT_DIR)/bin
	curl -sL https://github.com/elastic/crd-ref-docs/releases/download/v$(CRD_DOCS_VERSION)/crd-ref-docs_$(CRD_DOCS_VERSION)_$(shell uname)_$(CRD_DOCS_ARCH).tar.gz -o $(PROJECT_DIR)/tmp/crd-ref-docs.tar.gz \
		&& tar xzf $(PROJECT_DIR)/tmp/crd-ref-docs.tar.gz -C $(PROJECT_DIR)/bin \
		&& rm -f $(PROJECT_DIR)/tmp/crd-ref-docs.tar.gz

# Pattern-based rule for cloning GitHub repositories
$(GIT_BASE)/github.com/%:
	mkdir -p $(dir $@)
	@cd $(dir $@) && \
		if ! echo url=https://github.com | GIT_TERMINAL_PROMPT=0 git credential fill >/dev/null; then \
		  if [ -n "$(GH_TOKEN)" ]; then \
			echo "Using GH_TOKEN for GitHub authentication..."; \
			git clone https://$(GH_TOKEN):@github.com/$*.git; \
		  elif [ "$(GH_SSH)" = "true" ]; then \
		    echo "Using SSH keys for GitHub authentication..."; \
			git clone git@github.com:$*.git; \
		  fi \
		else \
		  git clone https://github.com/$*.git; \
		fi
