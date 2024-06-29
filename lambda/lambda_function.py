import json
import boto3
from datetime import datetime
import os
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']
uid_key = os.environ['UID_KEY']

def lambda_handler(event, context):
    try:

        body = json.loads(event['body'])

    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: JSON body not found in the request')
        }
    except json.decoder.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request: Invalid JSON format')
        }

    if not isinstance(body, list):
        body = [body]

    try:
        current_date = datetime.utcnow().strftime('%y/%m/%d')

        for document in body:
            
            if uid_key not in document:
                return {
                    'statusCode': 400,
                    'body': json.dumps(f'Bad Request: Unique identifier is missing in the document')
                }
            
            file_name = document[uid_key] + '.json'
            s3_key = f"{current_date}/{file_name}"

            overwrite = document.get('_overwrite', False)
            if isinstance(overwrite, str):
                overwrite = overwrite.lower() == 'true'
            
            # Check if the file already exists in S3
            try:
                s3_client.head_object(Bucket=bucket_name, Key=s3_key)
                file_exists = True
            except ClientError as e:
                if e.response['Error']['Code'] == '404':
                    file_exists = False
                else:
                    raise

            if file_exists and not overwrite:
                return {
                    'statusCode': 409,
                    'body': json.dumps(f'Conflict: File with key "{s3_key}" already exists and overwrite is set to False')
                }
            
            # Write to S3
            s3_client.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=json.dumps(document)
            )
            print(f"Wrote {file_name} to S3")

        return {
            'statusCode': 200,
            'body': json.dumps('Data successfully written to S3')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Internal Server Error: {str(e)}')
        }
