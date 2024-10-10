#!/usr/bin/env python3
import os

import aws_cdk as cdk,Environment

from cdk.cdk_stack import CdkStack

app = cdk.App()
CdkStack(app, "CdkStack",
    env=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region="us-east-1"))

app.synth()
