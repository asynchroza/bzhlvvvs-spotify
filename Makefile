.PHONY: aws-api
aws-api: 
	rm -rf .aws-sam && sam build && sam local start-api

.PHONY: aws-deploy
aws-deploy:
	rm -rf .aws-sam && sam build --use-container && sam deploy

.PHONY: pipeline-deploy
pipeline-deploy: 
	./write_env.sh && pip install -r src/requirements.txt && \
	pytest ./src && sam build --use-container && \
	sam deploy --no-fail-on-empty-changeset --no-confirm-changeset && \
	./health_check.sh

.PHONY: install-deps
install-deps:
	cd ./src && pip install -r requirements.txt -t ./ --upgrade