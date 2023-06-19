.PHONY: aws-api
aws-api: 
	rm -rf .aws-sam && sam build && sam local start-api

.PHONY: aws-deploy
aws-deploy:
	rm -rf .aws-sam && sam build --use-container && sam deploy

.PHONY: pipeline-deploy
pipeline-deploy: 
	pip install -r src/requirements.txt && pytest && sam build --use-container && sam deploy --no-fail-on-empty-changeset --no-confirm-changeset