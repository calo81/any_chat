# Any Chat Gradio Helm Chart

This Helm chart deploys a Gradio-based AI agent application using OpenAI Agents SDK with uv for package management.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+
- Docker registry access

## Installation

1. Build and push the Docker image:
```bash
docker build -t your-registry/any-chat-gradio:latest .
docker push your-registry/any-chat-gradio:latest
```

2. Install the Helm chart:
```bash
helm install my-any-chat ./helm-chart/any-chat-gradio \
  --set image.repository=your-registry/any-chat-gradio \
  --set app.env.OPENAI_API_KEY="your-openai-api-key"
```

## Configuration

The following table lists the configurable parameters of the chart and their default values.

### Application Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `app.env.OPENAI_API_KEY` | OpenAI API key for the agent | `""` |
| `app.env.RESOURCES` | Available resources for the agent | `"web_search,file_reader,code_interpreter"` |
| `app.env.TOOLS` | Available tools for the agent | `"search,analyze,generate"` |
| `app.env.GRADIO_SERVER_NAME` | Server bind address | `"0.0.0.0"` |
| `app.env.GRADIO_SERVER_PORT` | Server port | `"7860"` |

### Deployment Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `1` |
| `image.repository` | Image repository | `any-chat-gradio` |
| `image.tag` | Image tag | `latest` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `service.type` | Kubernetes service type | `ClusterIP` |
| `service.port` | Service port | `7860` |
| `resources.limits.cpu` | CPU limit | `1000m` |
| `resources.limits.memory` | Memory limit | `2Gi` |
| `resources.requests.cpu` | CPU request | `500m` |
| `resources.requests.memory` | Memory request | `1Gi` |

### Ingress Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable ingress | `false` |
| `ingress.className` | Ingress class name | `""` |
| `ingress.hosts` | Ingress hosts | `[{"host": "any-chat-gradio.local", "paths": [{"path": "/", "pathType": "Prefix"}]}]` |

## Examples

### Basic Installation with OpenAI API Key

```bash
helm install my-chat ./helm-chart/any-chat-gradio \
  --set app.env.OPENAI_API_KEY="sk-your-key-here"
```

### With Custom Resources and Tools

```bash
helm install my-chat ./helm-chart/any-chat-gradio \
  --set app.env.OPENAI_API_KEY="sk-your-key-here" \
  --set app.env.RESOURCES="web_search,database,api_calls" \
  --set app.env.TOOLS="search,query,generate,analyze"
```

### With Ingress Enabled

```bash
helm install my-chat ./helm-chart/any-chat-gradio \
  --set app.env.OPENAI_API_KEY="sk-your-key-here" \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host="chat.example.com"
```

### With Auto-scaling

```bash
helm install my-chat ./helm-chart/any-chat-gradio \
  --set app.env.OPENAI_API_KEY="sk-your-key-here" \
  --set autoscaling.enabled=true \
  --set autoscaling.minReplicas=2 \
  --set autoscaling.maxReplicas=10
```

## Uninstalling the Chart

To uninstall/delete the deployment:

```bash
helm uninstall my-any-chat
```

## License

This chart is licensed under the MIT License.