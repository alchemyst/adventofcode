docker-build:
    docker build -t adventofcode .

docker-run:
    docker run \
    -it \
    --name adventofcode \
    --mount type=bind,source="$(pwd)",target="/adventofcode" \
    adventofcode
        