FROM python:3.11-slim

# Install system dependencies required for SpiderFoot compilation and network scraping
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    gcc \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone production SpiderFoot branch, handle dependency installation, and enforce executable rights
RUN git clone https://github.com/smicallef/spiderfoot.git /app/spiderfoot \
    && pip install --no-cache-dir -r /app/spiderfoot/requirements.txt \
    && pip install --no-cache-dir watchdog \
    && chmod +x /app/spiderfoot/sf.py \
    && ln -s /app/spiderfoot/sf.py /usr/local/bin/sf.py

# Inject SpiderFoot home folder into the global execution PATH
ENV PATH="/app/spiderfoot:${PATH}"

# Copy our integrated system sentinel daemon into the workdir
COPY sentinel.py /app/sentinel.py

CMD ["python3", "/app/sentinel.py"]
