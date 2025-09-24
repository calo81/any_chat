#!/bin/bash

# Deploy script for Any Chat Gradio application
set -e

# Default values
IMAGE_REGISTRY=""
IMAGE_NAME="any-chat-gradio"
IMAGE_TAG="latest"
RELEASE_NAME="any-chat"
NAMESPACE="default"
OPENAI_API_KEY=""
CHART_PATH="./helm-chart/any-chat-gradio"

# Help function
show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

Deploy Any Chat Gradio application to Kubernetes using Helm.

OPTIONS:
    -r, --registry REGISTRY     Docker registry for the image
    -n, --name NAME            Release name (default: any-chat)
    -s, --namespace NAMESPACE  Kubernetes namespace (default: default)
    -k, --api-key KEY          OpenAI API key (required)
    -t, --tag TAG              Image tag (default: latest)
    --build                    Build and push Docker image before deploying
    --upgrade                  Upgrade existing release
    --dry-run                  Perform a dry run
    -h, --help                 Show this help message

EXAMPLES:
    # Deploy with OpenAI API key
    $0 --api-key "sk-your-key" --registry "your-registry.com"
    
    # Build, push and deploy
    $0 --api-key "sk-your-key" --registry "your-registry.com" --build
    
    # Upgrade existing deployment
    $0 --api-key "sk-your-key" --registry "your-registry.com" --upgrade

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--registry)
            IMAGE_REGISTRY="$2"
            shift 2
            ;;
        -n|--name)
            RELEASE_NAME="$2"
            shift 2
            ;;
        -s|--namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        -k|--api-key)
            OPENAI_API_KEY="$2"
            shift 2
            ;;
        -t|--tag)
            IMAGE_TAG="$2"
            shift 2
            ;;
        --build)
            BUILD_IMAGE=true
            shift
            ;;
        --upgrade)
            UPGRADE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option $1"
            show_help
            exit 1
            ;;
    esac
done

# Validate required parameters
if [[ -z "$OPENAI_API_KEY" ]]; then
    echo "Error: OpenAI API key is required. Use -k or --api-key"
    exit 1
fi

if [[ -z "$IMAGE_REGISTRY" ]]; then
    echo "Error: Docker registry is required. Use -r or --registry"
    exit 1
fi

# Construct full image name
FULL_IMAGE_NAME="${IMAGE_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"

# Build and push image if requested
if [[ "$BUILD_IMAGE" == "true" ]]; then
    echo "Building Docker image: $FULL_IMAGE_NAME"
    docker build -t "$FULL_IMAGE_NAME" .
    
    echo "Pushing Docker image: $FULL_IMAGE_NAME"
    docker push "$FULL_IMAGE_NAME"
fi

# Prepare Helm command
HELM_CMD="helm"
if [[ "$UPGRADE" == "true" ]]; then
    HELM_CMD="$HELM_CMD upgrade"
else
    HELM_CMD="$HELM_CMD install"
fi

HELM_CMD="$HELM_CMD $RELEASE_NAME $CHART_PATH"
HELM_CMD="$HELM_CMD --namespace $NAMESPACE"
HELM_CMD="$HELM_CMD --set image.repository=$IMAGE_REGISTRY/$IMAGE_NAME"
HELM_CMD="$HELM_CMD --set image.tag=$IMAGE_TAG"
HELM_CMD="$HELM_CMD --set app.env.OPENAI_API_KEY=$OPENAI_API_KEY"

if [[ "$DRY_RUN" == "true" ]]; then
    HELM_CMD="$HELM_CMD --dry-run --debug"
fi

# Execute Helm command
echo "Executing: $HELM_CMD"
eval "$HELM_CMD"

if [[ "$DRY_RUN" != "true" ]]; then
    echo ""
    echo "Deployment completed successfully!"
    echo ""
    echo "To check the status:"
    echo "  kubectl get pods -n $NAMESPACE -l app.kubernetes.io/instance=$RELEASE_NAME"
    echo ""
    echo "To access the application locally:"
    echo "  kubectl port-forward -n $NAMESPACE svc/$RELEASE_NAME-any-chat-gradio 7860:7860"
    echo "  Then open http://localhost:7860"
fi