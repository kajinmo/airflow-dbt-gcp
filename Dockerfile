# Base image
FROM python:3.12 AS build

RUN apt-get update && apt-get install -y build-essential curl
ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh
COPY ./requirements.txt .
RUN /root/.local/bin/uv venv /opt/venv && \
    /root/.local/bin/uv pip install --no-cache -r requirements.txt

# App image
FROM python:3.12-slim-bookworm
COPY --from=build /opt/venv /opt/venv

# Activate the virtualenv in the container
ENV PATH="/opt/venv/bin:$PATH"

# Copy all application files to the container 
COPY . /app
WORKDIR /app
CMD ["python", "main.py"]