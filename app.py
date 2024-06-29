import os
import aws_cdk as cdk
from api_gateway_lambda_s3.api_gateway_lambda_s3_stack import WebhookEventHandlerStack
from dotenv import load_dotenv
load_dotenv()

ACCOUNT_ID = os.getenv('ACCOUNT_ID')
REGION = os.getenv('REGION')

if not ACCOUNT_ID or not REGION:
    raise ValueError("Both AWS_ACCOUNT_ID and AWS_REGION environment variables must be set")

app = cdk.App()
WebhookEventHandlerStack(app, 
                        "WebhookEventHandlerStack",
                        uid_key='event_id',
                        env=cdk.Environment(account=ACCOUNT_ID, region=REGION)
    )

app.synth()
