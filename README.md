# Any Chat - AI Agent Kubernetes Deployment

Deploy an AI Agent about anything in Kubernetes using Gradio and OpenAI Agents SDK.

## 🚀 Features

- **Gradio Interface**: User-friendly web interface for interacting with AI agents
- **OpenAI Agents SDK**: Integration with OpenAI's powerful AI capabilities
- **uv Package Management**: Fast and reliable Python package management
- **Kubernetes Native**: Production-ready Helm chart for Kubernetes deployment
- **Configurable Environment**: Easy configuration via ConfigMaps
- **Auto-scaling**: Built-in HPA support for scaling based on demand
- **Ingress Support**: Optional ingress configuration for external access

## 📋 Prerequisites

- Kubernetes cluster (1.19+)
- Helm 3.2.0+
- Docker registry access
- OpenAI API key

## 🛠 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/calo81/any_chat.git
   cd any_chat
   ```

2. **Build the Docker image**:
   ```bash
   docker build -t your-registry/any-chat-gradio:latest .
   docker push your-registry/any-chat-gradio:latest
   ```

3. **Deploy with Helm**:
   ```bash
   helm install my-chat ./helm-chart/any-chat-gradio \
     --set image.repository=your-registry/any-chat-gradio \
     --set app.env.OPENAI_API_KEY="your-openai-api-key"
   ```

4. **Access the application**:
   ```bash
   kubectl port-forward svc/my-chat-any-chat-gradio 7860:7860
   ```
   Then open http://localhost:7860 in your browser.

## ⚙️ Configuration

### Environment Variables

The application supports the following environment variables via ConfigMap:

- **OPENAI_API_KEY**: Your OpenAI API key (required)
- **RESOURCES**: Available resources for the agent (default: "web_search,file_reader,code_interpreter")
- **TOOLS**: Available tools for the agent (default: "search,analyze,generate")
- **GRADIO_SERVER_NAME**: Server bind address (default: "0.0.0.0")
- **GRADIO_SERVER_PORT**: Server port (default: "7860")

### Helm Values

See [helm-chart/README.md](helm-chart/README.md) for detailed configuration options.

## 📁 Project Structure

```
any_chat/
├── app/                    # Application source code
│   └── main.py            # Main Gradio application
├── helm-chart/            # Helm chart
│   └── any-chat-gradio/   # Chart files
│       ├── Chart.yaml     # Chart metadata  
│       ├── values.yaml    # Default values
│       └── templates/     # Kubernetes templates
├── Dockerfile             # Container image definition
├── pyproject.toml         # Python project configuration
├── uv.lock               # Dependency lock file
└── README.md             # This file
```

## 🔧 Development

### Local Development

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Set environment variables**:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   export RESOURCES="web_search,file_reader,code_interpreter"
   export TOOLS="search,analyze,generate"
   ```

3. **Run the application**:
   ```bash
   uv run python app/main.py
   ```

### Testing Helm Chart

```bash
# Lint the chart
helm lint helm-chart/any-chat-gradio/

# Test template rendering
helm template test helm-chart/any-chat-gradio/ \
  --set app.env.OPENAI_API_KEY="test-key"

# Dry run installation
helm install test helm-chart/any-chat-gradio/ \
  --set app.env.OPENAI_API_KEY="test-key" \
  --dry-run --debug
```

## 🚀 Production Deployment

For production deployments, see [helm-chart/any-chat-gradio/values-example.yaml](helm-chart/any-chat-gradio/values-example.yaml) for a complete configuration example including:

- Ingress with TLS
- Resource limits and requests  
- Auto-scaling configuration
- Node affinity rules
- Security contexts

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
