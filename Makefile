.PHONY: aws-api
aws-api: 
	rm -rf .aws-sam && sam local start-api