# Using Ollama with Docker (Without Administrator Permissions)

Since we don't have administrator (sudo) permissions, we use Docker for running Ollama, follow these steps. This method assumes Docker is already installed and your user has permissions to run Docker commands (i.e., you’re in the docker group).

---

## Step 1: Pull the Ollama Docker Image
Download the official Ollama Docker image:
```bash
docker pull ollama/ollama
```

## Step 2: Run the Ollama Container
Start a detached (background) container with persistent storage for models:

```bash
docker run -d \
  --name ollama \
  -v ~/.ollama:/root/.ollama \
  -p 11434:11434 \
  ollama/ollama
```

`-d`: Run the container in the background.

`--name ollama`: Name the container for easy reference.

`-v ~/.ollama:/root/.ollama`: Maps the local ~/.ollama directory (on your machine) to the container’s model storage.

`-p 11434:11434`: Exposes port 11434 for API access.

## Step 3: Interact with Ollama
Use docker exec to run commands inside the container. For example:

Run a Model (e.g., llama2):

```bash
docker exec -it ollama ollama run llama2
docker exec -it ollama ollama run deepseek-r1:8b
docker exec -it ollama ollama run nomic-embed-text
```
This downloads the model (if not cached) and starts a chat session.

List Downloaded Models:

```bash
docker exec -it ollama ollama list
```

Remove a model:

```bash
docker exec -it ollama ollama rm <model-name>
```