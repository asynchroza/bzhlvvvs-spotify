.PHONY: aws-api
aws-api: 
	rm -rf .aws-sam && sam build && sam local start-api