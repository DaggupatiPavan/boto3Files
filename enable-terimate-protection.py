import boto3

# Create an EC2 client
ec2_client = boto3.client('ec2')

# Describe all instances to get their instance IDs and states
response = ec2_client.describe_instances()

# Loop through each instance and enable termination protection for running or stopped instances
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        state = instance['State']['Name']
        if state in ['running', 'stopped']:
            ec2_client.modify_instance_attribute(
                InstanceId=instance_id,
                DisableApiTermination={'Value': True}
            )
            print(f"Termination protection enabled for instance {instance_id} (state: {state})")

print("Termination protection enabled for all running or stopped instances.")
