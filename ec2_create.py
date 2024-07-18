import boto3

# Initialize a session using Amazon EC2
ec2 = boto3.client('ec2')

# Variables
instance_name = 'marvel-boto3-test'
instance_type = "t3.micro"

security_group_id = 'sg-0d56e86ef61a7dc01'  
key_name = 'nextgen-devops-team'
subnet_id = 'subnet-00cef52dd64304b35' #private_subnet4
# subnet_id = 'subnet-0f741dbdc133a669c' #private_subnet3
# subnet_id = 'subnet-02cf2e19298b8cdac' #private_subnet2
# subnet_id = 'subnet-09bb946c638fdd9a3' #private_subnet1

# Create a new EC2 instance
instances = ec2.run_instances(
    ImageId='ami-04a81a99f5ec58529',  # ubuntu 24.02
    MinCount=1,
    MaxCount=1,
    InstanceType=instance_type,
    KeyName=key_name,
    SecurityGroupIds=[security_group_id],
    SubnetId=subnet_id,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': instance_name
                }
            ]
        }
    ]
)
print("Instance created with ID:", instances['Instances'][0]['InstanceId'])
print("Instance created with Name:", instance_name)

ec2.modify_instance_attribute(
    InstanceId=instance_id,
    DisableApiTermination={
        'Value': True
    }
)

print(f"Termination protection enabled for instance {instance_id}")
