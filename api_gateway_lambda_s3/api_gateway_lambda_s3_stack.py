from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_logs as logs
)
from aws_cdk.aws_apigatewayv2 import HttpApi, HttpMethod
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
from constructs import Construct
import aws_cdk as core

class WebhookEventHandlerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, uid_key: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an S3 bucket
        bucket = s3.Bucket(self, 
                           "EventWebhooksBucket", 
                           removal_policy=core.RemovalPolicy.DESTROY,
                           bucket_name='event-webhooks-bucket')

        # Create a Lambda function
        lambda_function = _lambda.Function(
            self, 
            "EventProcessingLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "UID_KEY": uid_key
            }
        )

        # Grant Lambda permissions to write to the S3 bucket
        bucket.grant_write(lambda_function)

        # Grant Lambda permissions to read objects and perform head_object
        bucket.grant_read(lambda_function)

        # Configuring Cloud Watch Logs
        logs.LogGroup(self, "MyLambdaLogGroup",
            log_group_name=f"/aws/lambda/{lambda_function.function_name}",
            retention=logs.RetentionDays.ONE_WEEK
        )

        # Create an HTTP API and integrate it with the Lambda function
        http_api = HttpApi(
            self, 
            "EventHttpApi"
        )

        # Create an integration for the Lambda function
        lambda_integration = HttpLambdaIntegration(
            "EventProcessingLambdaIntegration",
            handler=lambda_function
        )

        # Add a POST method to the /events route
        http_api.add_routes(
            path="/events",
            methods=[HttpMethod.POST],
            integration=lambda_integration
        )