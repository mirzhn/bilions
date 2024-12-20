git clone https://github.com/apache/superset
cd superset
docker compose -f docker-compose-image-tag.yml up

#docker-compose-image-tag.yml
command:
      - /bin/bash
      - -c
      - |
        pip install clickhouse-connect &&
        /app/docker/docker-bootstrap.sh app-gunicorn


docker network create superset_clickhouse_network


python3 ./generate/_main_generator.py
python3 ./upload/load_to_click.py