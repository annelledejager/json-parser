# Pull base image
FROM python:3

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Define working directory
RUN mkdir /app
WORKDIR /app

# Install
ADD requirements.txt /app/
RUN pip install -r requirements.txt

# Install
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]
RUN ["apt-get", "install", "-y", "postgresql"]
RUN ["apt-get", "install", "-y", "postgresql-contrib"]

ADD . /app/

# Set entrypoint
RUN chmod +x ./scripts/docker-entrypoint.sh
ENTRYPOINT ["./scripts/docker-entrypoint.sh"]

CMD [""]
