remove:
		docker rm -f trade-producer-image

build:
		docker build -t trade-producer .

run: remove build
		docker run -it --network redpanda_network --name trade-producer-image trade-producer

stop:
		docker stop trade-producer-image

lint:
		ruff check --fix

format:
		ruff format .
