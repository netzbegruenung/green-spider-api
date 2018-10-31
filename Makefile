docker-build:
	docker build -t quay.io/netzbegruenung/green-spider-api .

docker-run:
	docker run --rm \
		-p 5000:5000 \
		-v $(shell pwd)/secrets:/secrets \
		-e GCLOUD_DATASTORE_CREDENTIALS_PATH=/secrets/green-spider-api.json \
		quay.io/netzbegruenung/green-spider-api
