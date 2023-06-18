import json

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "courses": [
                    {
                        "id": "1001",
                        "name": "Introduction to C++",
                        "description": "Introductionary programming course",
                        "start_date": "2023-06-17T21:00:00.000Z",
                        "end_date": "2023-06-17T21:00:00.000Z",
                        "instructor_id": 1,
                        "department_id": "COS",
                    }
                ]
            }
        ),
    }
