FROM python:3.14-slim

RUN pip install uv

COPY . .

WORKDIR /app/

RUN uv sync

CMD ["uv", "run", "main.py"]