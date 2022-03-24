check-user:
ifndef USER_NAME
	$(error Please provide a user name with building/pushing a Docker image (e.g. make USER_NAME=<your-name> docker-build))
endif

.PHONY: check
check: format
	poetry run pre-commit run --all

.PHONY: docker-build
docker-build: check-user
	docker build -t europe-west3-docker.pkg.dev/gdd-vertex/docker/fashion-${USER_NAME} .

.PHONY: docker-run
docker-run: docker-build
	docker run --rm -it europe-west3-docker.pkg.dev/gdd-vertex/docker/fashion-${USER_NAME} fancy-fashion --help

.PHONY: docker-push
docker-push: docker-build
	docker push europe-west3-docker.pkg.dev/gdd-vertex/docker/fashion-${USER_NAME}

.PHONY: format
format:
	poetry run black .


