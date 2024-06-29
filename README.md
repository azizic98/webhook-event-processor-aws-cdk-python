# Webhook Event Handler CDK Stack

This AWS CDK stack sets up an architecture involving an S3 bucket, a Lambda function, and an HTTP API. The Lambda function processes JSON data received through the API and writes it to the S3 bucket.

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Set Up a Virtual Environment](#2-set-up-a-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Set Up Environment Variables](#4-set-up-environment-variables)
  - [5. Deploy the Stack](#5-deploy-the-stack)
- [Customization](#customization)
- [Usage](#usage)
- [Clean Up](#clean-up)
- [License](#license)

## Architecture Overview

This CDK stack provisions the following resources:
- An S3 bucket to store JSON data.
- A Lambda function that processes incoming JSON data and writes it to the S3 bucket.
- An HTTP API (API Gateway) that triggers the Lambda function via HTTP POST requests.

## Prerequisites

Before you begin, ensure you have the following installed:
- [AWS CLI](https://aws.amazon.com/cli/)
- [AWS CDK](https://aws.amazon.com/cdk/)
- [Python 3.8](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/en/download/) (for AWS CDK)

## Setup Instructions

### 1. Clone the Repository

```sh
git clone <repository-url>
cd <repository-directory>
```

### 2. Set Up a Virtual Environment

Create and activate a virtual environment:

#### On macOS/Linux

```sh
python3 -m venv .venv
source .venv/bin/activate
```

#### On Windows

```sh
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages using `pip`:

```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root of your project directory and add your AWS Account ID and region. You can retrieve your AWS Account ID using the AWS CLI:

```sh
aws sts get-caller-identity --query Account --output text
```

Your `.env` file should look like this:

```dotenv
ACCOUNT_ID=your_account_id
REGION=your_region
```

### 5. Deploy the Stack

Run the following commands to deploy the CDK stack:

```sh
cdk bootstrap
cdk deploy
```

## Customization

### Configuring `uid_key`

In `app.py`, set the `uid_key` parameter to the unique identifier present in your webhook payloads:

```python
WebhookEventHandlerStack(app, 
                         "WebhookEventHandlerStack",
                         uid_key='event_id',  # Replace 'event_id' with your unique identifier
                         env=cdk.Environment(account=ACCOUNT_ID, region=REGION)
)
```

### Customizing the S3 Bucket Name

You can customize the S3 bucket name in `api_gateway_lambda_s3_stack.py`:

```python
bucket = s3.Bucket(self, 
                   "EventWebhooksBucket", 
                   removal_policy=core.RemovalPolicy.DESTROY,
                   bucket_name='your-custom-bucket-name')
```

## Usage

Once the stack is deployed, you can send POST requests to the API endpoint with your JSON data. The data will be processed by the Lambda function and stored in the S3 bucket.

Example POST request using `curl`:

```sh
curl -X POST <api-endpoint>/events -H "Content-Type: application/json" -d '{"event_id": "12345", "data": "example"}'
```

Replace `<api-endpoint>` with the URL of your deployed API Gateway.

## Clean Up

To delete the stack and all associated resources, run:

```sh
cdk destroy
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
