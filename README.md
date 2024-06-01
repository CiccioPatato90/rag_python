
# RAG Python

## Overview

RAG Python is a project that leverages Retrieval-Augmented Generation (RAG) to enhance the capabilities of language models. The system is designed to be efficient, reliable, and scalable by using a startup chain with Docker Compose and an orchestrator. This approach ensures that models and services are initialized only once, optimizing performance and resource utilization.

## Features

- **Efficient Initialization**: Components are started only once, reducing overhead.
- **Scalable Architecture**: Uses Docker Compose for easy scaling and management.
- **Real-Time Communication**: Integrates WebSockets for bi-directional communication.
- **Persistent Storage**: Utilizes databases to store and retrieve data effectively.
- **Embedding Model**: Initializes and uses an embedding model for transforming input data into vectors.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Python 3.8+

### Installation

1. **Clone the repository**:
   \`\`\`bash
   git clone https://github.com/CiccioPatato90/rag_python.git
   cd rag_python
   \`\`\`

2. **Set up the environment**:
   Ensure you have Docker and Docker Compose installed on your machine.

3. **Start the Docker Compose services**:
   \`\`\`bash
   docker-compose up -d
   \`\`\`

4. **Initialize the Embedding Model**:
   \`\`\`bash
   python initialize_embedding_model.py
   \`\`\`

## Usage

Once the services are up and running, you can interact with the system through the provided APIs and WebSocket endpoints. The models and services are pre-initialized to ensure fast and efficient processing of requests.

### API Endpoints

- **/api/query**: Endpoint to submit queries and get responses from the LLM.
- **/api/status**: Endpoint to check the status of various services.

### WebSocket Endpoints

- **/ws/chat**: WebSocket endpoint for real-time chat interactions with the LLM.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please open an issue on the GitHub repository.
