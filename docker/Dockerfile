FROM sinapsis-nvidia:base

RUN apt-get update && apt-get install -y ffmpeg git && rm -rf /var/lib/apt/lists/*
COPY . /app/
WORKDIR /app
RUN uv sync --frozen  --extra cotracker
RUN uv pip install sinapsis-trackers[all] --extra-index-url https://pypi.sinapsis.tech