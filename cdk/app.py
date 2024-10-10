#!/usr/bin/env python3
import os

from aws_cdk import App, Environment

from cdk.cdk_stack import CdkStack

app = App()
CdkStack(app, "CdkStack",
    env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region="us-east-1")
)

app.synth()
