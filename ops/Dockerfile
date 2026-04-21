FROM python:3.14-slim

RUN pip install uv

COPY . /workspace

WORKDIR /workspace

RUN UV_PROJECT_ENVIRONMENT=/opt/venv uv sync

# Create directories
RUN mkdir -p /workspace/input /workspace/output

# Default: bash shell for running commands
CMD ["/bin/bash"]