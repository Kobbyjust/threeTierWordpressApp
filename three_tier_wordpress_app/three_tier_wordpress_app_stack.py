from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_dynamodb as dynamodb,
)
  
    
from . import config



class ThreeTierWordpressAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #creating dynamodb table
        # table = dynamodb.Table(
        # self, "threeTierDB",
        # partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
        # sort_key=dynamodb.Attribute(name="date", type=dynamodb.AttributeType.NUMBER),
        # billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        # )

        igw_id = ec2.Vpc.internet_gateway_id

        myinstanceVPC = ec2.Vpc(self, 'MyTreeTierVPC',
          ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
        
        # 'maxAzs' configures the maximum number of availability zones to use
          max_azs=3,

        # 'subnetConfiguration' specifies the "subnet groups" to create.
        # Every subnet group will have a subnet for each AZ, so this
        # 'name' is used to name this particular subnet group. 
        # You will have to use the name for subnet selection if you have more than one subnet group of the same type.
        
        subnet_configuration=[ec2.SubnetConfiguration(
            subnet_type=ec2.SubnetType.PUBLIC,
            availability_zones=["us-east-1a", "us-east-1b"],
            name="myAppLayer",
            cidr_mask=24
        ),
        ec2.SubnetConfiguration(
        cidr_mask=24,
        name="Application",
        subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
        availability_zones=["us-east-1a", "us-east-1b"],
        ),
        ],

        #adding access to an internet gateway
        igw_id = igw_id,
        )

        #My security Groups
        my_security_group = ec2.SecurityGroup(self, "SecurityGroup",
        vpc=myinstanceVPC,
        description="Allow ssh access to ec2 instances",
        allow_all_outbound=True
        )
        my_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow ssh access from the world")

        
