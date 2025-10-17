.PHONY: help build push clean

IMAGE_NAME = quay.io/jmelis/openmeteo-exporter
TAG ?= latest

# Container runtime detection: prefer podman, fallback to docker
CONTAINER_RUNTIME ?= $(shell command -v podman 2>/dev/null || command -v docker 2>/dev/null)

# If user wants to override, they can set CONTAINER_RUNTIME=docker
ifeq ($(CONTAINER_RUNTIME),)
$(error No container runtime found. Please install podman or docker)
endif

help:
	@echo "Open-Meteo Exporter - Available targets:"
	@echo "  build         - Build the container image"
	@echo "  push          - Push the container image to quay.io"
	@echo "  clean         - Remove the container image"
	@echo ""
	@echo "Container runtime: $(notdir $(CONTAINER_RUNTIME))"
	@echo ""
	@echo "Usage examples:"
	@echo "  make build"
	@echo "  make push"
	@echo "  make build push"
	@echo "  make TAG=v1.0.0 build push"
	@echo ""
	@echo "To override container runtime:"
	@echo "  make CONTAINER_RUNTIME=docker build"
	@echo "  make CONTAINER_RUNTIME=podman build"

build:
	@echo "Building container image: $(IMAGE_NAME):$(TAG)"
	@echo "Using: $(notdir $(CONTAINER_RUNTIME))"
	$(CONTAINER_RUNTIME) build --platform linux/amd64 -t $(IMAGE_NAME):$(TAG) .
	@echo "✓ Build complete"

push: build
	@echo "Pushing container image: $(IMAGE_NAME):$(TAG)"
	@echo "Using: $(notdir $(CONTAINER_RUNTIME))"
	$(CONTAINER_RUNTIME) push $(IMAGE_NAME):$(TAG)
	@echo "✓ Push complete"

clean:
	@echo "Removing container image: $(IMAGE_NAME):$(TAG)"
	@echo "Using: $(notdir $(CONTAINER_RUNTIME))"
	$(CONTAINER_RUNTIME) rmi $(IMAGE_NAME):$(TAG) || true
	@echo "✓ Image removed"
