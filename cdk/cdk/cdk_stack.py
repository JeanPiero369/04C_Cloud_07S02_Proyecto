from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnOutput,
    CfnParameter,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancingv2_targets as targets,
    Duration
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account_id = kwargs.get('env').account

        # Parameters

        ami_id = CfnParameter(self, "AMI",
            type="String",
            default="ami-061eaf73cf9ce7d78",
            description="ID de AMI"
        )

        # Security Group
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)

        # Updated IAM Role ARN with new Account ID
        existing_role_arn = f"arn:aws:iam::{account_id}:role/LabRole"
        role = iam.Role.from_role_arn(self, "ExistingRole", existing_role_arn)

        security_group_produccion = ec2.SecurityGroup(self, "GS Produccion",
            vpc=vpc,
            security_group_name="Proyecto - GS Produccion",
            description="Permitir trafico SSH y HTTP desde cualquier lugar",
            allow_all_outbound=True
        )

        security_group_produccion.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH")
        security_group_produccion.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP")
        security_group_produccion.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(8000), "Allow Traffic on Port 8000")
        security_group_produccion.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(8001), "Allow Traffic on Port 8001")
        security_group_produccion.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(8002), "Allow Traffic on Port 8002")
        security_group_produccion.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(8003), "Allow Traffic on Port 8003")
        
        security_group_bd_datos = ec2.SecurityGroup(self, "GS Base de datos",
            vpc=vpc,
            security_group_name="Proyecto - GS Base de datos",
            description="Permitir trafico SSH y HTTP desde cualquier lugar",
            allow_all_outbound=True
        )

        security_group_bd_datos.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH")
        security_group_bd_datos.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(8080), "Allow Traffic on Port 8000")
        security_group_bd_datos.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(8000), "Allow Traffic on Port 8001")
        security_group_bd_datos.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(8001), "Allow Traffic on Port 8002")
        security_group_bd_datos.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(8002), "Allow Traffic on Port 8002")
        security_group_bd_datos.add_ingress_rule(ec2.Peer.security_group_id(security_group_produccion.security_group_id), ec2.Port.tcp(8000), "Allow Traffic on Port 8000")
        security_group_bd_datos.add_ingress_rule(ec2.Peer.security_group_id(security_group_produccion.security_group_id), ec2.Port.tcp(8001), "Allow Traffic on Port 8001")
        security_group_bd_datos.add_ingress_rule(ec2.Peer.security_group_id(security_group_produccion.security_group_id), ec2.Port.tcp(8002), "Allow Traffic on Port 8002")

        # EC2 Instance
        ec2_bd_datos = ec2.Instance(self, "MV Base de datos",
            vpc=vpc,
            instance_name="Proyecto - MV Base de datos",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.generic_linux({"us-east-1": ami_id.value_as_string}),
            security_group=security_group_bd_datos,
            key_name="vockey",
            block_devices=[ec2.BlockDevice(
                device_name="/dev/sda1",
                volume=ec2.BlockDeviceVolume.ebs(20)
            )],
            role=role,
        )

        ec2_produccion_01 = ec2.Instance(self, "MV Produccion 01",
            vpc=vpc,
            instance_name="Proyecto - MV Produccion 01",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.generic_linux({"us-east-1": ami_id.value_as_string}),
            security_group=security_group_produccion,
            key_name="vockey",
            block_devices=[ec2.BlockDevice(
                device_name="/dev/sda1",
                volume=ec2.BlockDeviceVolume.ebs(20)
            )],
            role=role,
            availability_zone="us-east-1a" 
        )

        ec2_produccion_02 = ec2.Instance(self, "MV Produccion 02",
            vpc=vpc,
            instance_name="Proyecto - MV Produccion 02",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.generic_linux({"us-east-1": ami_id.value_as_string}),
            security_group=security_group_produccion,
            key_name="vockey",
            block_devices=[ec2.BlockDevice(
                device_name="/dev/sda1",
                volume=ec2.BlockDeviceVolume.ebs(20)
            )],
            role=role,
            availability_zone="us-east-1b" 
        )

        ec2_ingesta = ec2.Instance(self, "MV Ingesta",
            vpc=vpc,
            instance_name="Proyecto - MV Ingesta",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.generic_linux({"us-east-1": ami_id.value_as_string}),
            security_group=security_group_bd_datos,
            key_name="vockey",
            block_devices=[ec2.BlockDevice(
                device_name="/dev/sda1",
                volume=ec2.BlockDeviceVolume.ebs(20)
            )],
            role=role
        )

        # Crear un Target Group para las instancias de Producción
        target_group_produccion_8000 = elbv2.ApplicationTargetGroup(self, "TG Produccion 8000",
            vpc=vpc,
            target_type=elbv2.TargetType.INSTANCE,
            protocol=elbv2.ApplicationProtocol.HTTP,
            port=8000,
            health_check=elbv2.HealthCheck(
                path="/",  # Ajusta esto según tu aplicación
                interval=Duration.seconds(30)
            ),
            target_group_name="Proyecto-TG-Produccion-8000"
        )

        target_group_produccion_8001 = elbv2.ApplicationTargetGroup(self, "TG Produccion 8001",
            vpc=vpc,
            target_type=elbv2.TargetType.INSTANCE,
            protocol=elbv2.ApplicationProtocol.HTTP,
            port=8001,
            health_check=elbv2.HealthCheck(
                path="/",  # Ajusta esto según tu aplicación
                interval=Duration.seconds(30)
            ),
            target_group_name="Proyecto-TG-Produccion-8001"
        )

        target_group_produccion_8002 = elbv2.ApplicationTargetGroup(self, "TG Produccion 8002",
            vpc=vpc,
            target_type=elbv2.TargetType.INSTANCE,
            protocol=elbv2.ApplicationProtocol.HTTP,
            port=8002,
            health_check=elbv2.HealthCheck(
                path="/",  # Ajusta esto según tu aplicación
                interval=Duration.seconds(30)
            ),
            target_group_name="Proyecto-TG-Produccion-8002"
        )

        target_group_produccion_8003 = elbv2.ApplicationTargetGroup(self, "TG Produccion 8003",
            vpc=vpc,
            target_type=elbv2.TargetType.INSTANCE,
            protocol=elbv2.ApplicationProtocol.HTTP,
            port=8003,
            health_check=elbv2.HealthCheck(
                path="/api/check_api",  # Ajusta esto según tu aplicación
                interval=Duration.seconds(30)
            ),
            target_group_name="Proyecto-TG-Produccion-8003"
        )

        # Asociar instancias al Target Group
        for target_group in {target_group_produccion_8000,target_group_produccion_8001,target_group_produccion_8002,target_group_produccion_8003}:
            for ec2_instance in {ec2_produccion_01,ec2_produccion_02}:
                target_group.add_target(targets.InstanceTarget(ec2_instance))

        # Crear el Load Balancer
        load_balancer = elbv2.ApplicationLoadBalancer(self, "LB Produccion",
            vpc=vpc,
            internet_facing=True,
            security_group=security_group_produccion,
            load_balancer_name="Proyecto-LB-Produccion",
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC,
                availability_zones=["us-east-1a", "us-east-1b"] 
            )
        )

        # Crear listeners para cada puerto
        listener_8000 = load_balancer.add_listener("Listener8000", port=8000, open=True,protocol=elbv2.ApplicationProtocol.HTTP)
        listener_8001 = load_balancer.add_listener("Listener8001", port=8001, open=True,protocol=elbv2.ApplicationProtocol.HTTP)
        listener_8002 = load_balancer.add_listener("Listener8002", port=8002, open=True,protocol=elbv2.ApplicationProtocol.HTTP)
        listener_8003 = load_balancer.add_listener("Listener8003", port=8003, open=True,protocol=elbv2.ApplicationProtocol.HTTP)

        # Agregar los Target Groups a cada Listener
        listener_8000.add_target_groups("TargetGroup8000", target_groups=[target_group_produccion_8000])
        listener_8001.add_target_groups("TargetGroup8001", target_groups=[target_group_produccion_8001])
        listener_8002.add_target_groups("TargetGroup8002", target_groups=[target_group_produccion_8002])
        listener_8003.add_target_groups("TargetGroup8003", target_groups=[target_group_produccion_8003])
        
        ip_privada = ec2_bd_datos.instance_private_ip

        ec2_ingesta.node.add_dependency(ec2_bd_datos)  # La ingesta depende de la base de datos
        ec2_produccion_01.node.add_dependency(ec2_ingesta)
        ec2_produccion_02.node.add_dependency(ec2_ingesta)

        ec2_bd_datos.add_user_data(
            "#!/bin/bash",
            "docker run -d --rm --name mysql_c -e MYSQL_ROOT_PASSWORD=utec -p 8000:3306 -v mysql_data:/var/lib/mysql mysql:8.0",
            "docker run -d --rm --name adminer_c -p 8080:8080 adminer",
            "docker run -d --rm --name postgres_c -e POSTGRES_PASSWORD=utec -p 8001:5432 -v postgres_data:/var/lib/postgresql/data postgres:14",
            "docker run -d --rm --name mongo_c -p 8002:27017 -v mongo_data:/data/db mongo:latest",
        )

        ec2_ingesta.add_user_data(
            "#!/bin/bash",
            "cd /home/ubuntu/",
            "git clone https://github.com/JeanPiero369/04C_Cloud_07S02_Proyecto.git",
            "cd ./04C_Cloud_07S02_Proyecto/data",
            f"echo 'DB_HOST={ip_privada}' > .env",  # Usar comillas simples
            "docker compose up -d",
        )

        ec2_produccion_01.add_user_data(
            "#!/bin/bash",
            "cd /home/ubuntu/",
            "git clone https://github.com/JeanPiero369/04C_Cloud_07S02_Proyecto.git",
            "cd ./04C_Cloud_07S02_Proyecto",
            f"echo 'DB_HOST={ip_privada}' > .env",  # Usar comillas simples
            "docker compose up -d",
        )

        ec2_produccion_02.add_user_data(
            "#!/bin/bash",
            "cd /home/ubuntu/",
            "git clone https://github.com/JeanPiero369/04C_Cloud_07S02_Proyecto.git",
            "cd ./04C_Cloud_07S02_Proyecto",
            f"echo 'DB_HOST={ip_privada}' > .env",  # Usar comillas simples
            "docker compose up -d",
        )

        #Outputs
        CfnOutput(self, "LoadBalancerDNS",
            description="DNS del Load Balancer",
            value=load_balancer.load_balancer_dns_name
        )

        #Outputs
        CfnOutput(self, "LoadBalancerDNS:orquestador",
            description="DNS del Load Balancer",
            value=f"{load_balancer.load_balancer_dns_name}:8000"
        )

        #Outputs
        CfnOutput(self, "LoadBalancerDNS:clientes",
            description="DNS del Load Balancer",
            value=f"{load_balancer.load_balancer_dns_name}:8001"
        )

        #Outputs
        CfnOutput(self, "LoadBalancerDNS:polizas",
            description="DNS del Load Balancer",
            value=f"{load_balancer.load_balancer_dns_name}:8002"
        )

        #Outputs
        CfnOutput(self, "LoadBalancerDNS:bienes",
            description="DNS del Load Balancer",
            value=f"{load_balancer.load_balancer_dns_name}:8003"
        )

        CfnOutput(self, "Base de datos - adminer",
            description="Adminer",
            value=f"http://{ec2_bd_datos.instance_public_ip}:8080"
        )
