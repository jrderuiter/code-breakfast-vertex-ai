check-user:
ifndef USER_NAME
	$(error Please provide a user name with building/pushing a Docker image (e.g. make USER_NAME=<your-name> docker-build))
endif

.PHONY: docker-init
docker-init:
	gcloud auth configure-docker europe-west3-docker.pkg.dev

.PHONY: docker-build
docker-build: check-user
	docker build -t europe-west3-docker.pkg.dev/gdd-cb-vertex/docker/fancy-fashion-${USER_NAME} .

.PHONY: docker-run
docker-run: docker-build
	docker run --rm -it europe-west3-docker.pkg.dev/gdd-cb-vertex/docker/fancy-fashion-${USER_NAME} fancy-fashion --help

.PHONY: docker-push
docker-push: docker-build
	docker push europe-west3-docker.pkg.dev/gdd-cb-vertex/docker/fancy-fashion-${USER_NAME}

.PHONY: python-init
python-init:
	poetry env use /opt/conda/envs/python3.9/bin/python
	poetry install

.PHONY: python-format
python-format:
	poetry run black src tests

.PHONY: python-lint
python-lint:
	poetry run pre-commit run --all

.PHONY: python-test
python-test:
	poetry run pytest

.PHONY: generate-data
generate-data: python-init
	poetry run scripts/generate_data.py && gsutil -m cp -r ./data/ gs://gdd-cb-vertex-fashion-inputs/
