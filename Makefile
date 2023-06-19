.PHONY: aws-api
aws-api: 
	rm -rf .aws-sam && sam build && sam local start-api

.PHONY: aws-deploy
aws-deploy:
	rm -rf .aws-sam && sam build --use-container && sam deploy