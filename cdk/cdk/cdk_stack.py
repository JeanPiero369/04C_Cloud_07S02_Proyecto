from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnOutput,
    CfnParameter
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account_id = kwargs.get('env').account

        # Parameters
        instance_name = CfnParameter(self, "InstanceName",
            type="String",
            default="MV Reemplazar",
            description="Nombre de la instancia a crear"
        )

        ami_id = CfnParameter(self, "AMI",
            type="String",
            default="ami-0aa28dab1f2852040",
            description="ID de AMI"
        )

        # Security Group
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)

        security_group = ec2.SecurityGroup(self, "InstanceSecurityGroup",
            vpc=vpc,
            description="Permitir trafico SSH y HTTP desde cualquier lugar",
            allow_all_outbound=True
        )

        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH")
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP")

        # Updated IAM Role ARN with new Account ID
        existing_role_arn = f"arn:aws:iam::{account_id}:role/LabRole"
        role = iam.Role.from_role_arn(self, "ExistingRole", existing_role_arn)

        # EC2 Instance
        ec2_instance = ec2.Instance(self, "EC2Instance",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.generic_linux({"us-east-1": ami_id.value_as_string}),
            security_group=security_group,
            key_name="vockey",
            block_devices=[ec2.BlockDevice(
                device_name="/dev/sda1",
                volume=ec2.BlockDeviceVolume.ebs(20)
            )],
            role=role
        )

        ec2_instance.add_user_data(
            "#!/bin/bash",
            "cd /var/www/html/",
            "git clone https://github.com/utec-cc-2024-2-test/websimple.git",
            "git clone https://github.com/utec-cc-2024-2-test/webplantilla.git",
            "ls -l"
        )

        # Outputs
        CfnOutput(self, "InstanceId",
            description="ID de la instancia EC2",
            value=ec2_instance.instance_id
        )

        CfnOutput(self, "InstancePublicIP",
            description="IP publica de la instancia",
            value=ec2_instance.instance_public_ip
        )

        CfnOutput(self, "websimpleURL",
            description="URL de websimple",
            value=f"http://{ec2_instance.instance_public_ip}/websimple"
        )

        CfnOutput(self, "webplantillaURL",
            description="URL de webplantilla",
            value=f"http://{ec2_instance.instance_public_ip}/webplantilla"
        )
