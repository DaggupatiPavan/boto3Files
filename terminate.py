import boto3

# Initialize a session using Amazon EC2
ec2 = boto3.client('ec2')

# List of instance IDs to terminate
instance_ids = ['instance-1','instance-2']  # Replace with your instance IDs

def disable_termination_protection(instance_id):
    ec2.modify_instance_attribute(
        InstanceId=instance_id,
        DisableApiTermination={
            'Value': False
        }
    )
    print(f"Termination protection disabled for instance {instance_id}")

def get_instance_name(instance_id):
    response = ec2.describe_instances(InstanceIds=[instance_id])
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            for tag in instance.get('Tags', []):
                if tag['Key'] == 'Name':
                    return tag['Value']
    return 'Unknown'

def check_and_terminate(instance_ids):
    instances_to_terminate = []
    for instance_id in instance_ids:
        response = ec2.describe_instance_attribute(
            InstanceId=instance_id,
            Attribute='disableApiTermination'
        )
        termination_protection = response['DisableApiTermination']['Value']
        
        if termination_protection:
            instance_name = get_instance_name(instance_id)
            user_input = input(f"Instance {instance_name} ({instance_id}) has termination protection enabled. Do you want to disable it and terminate the instance? (yes/no): ")
            if user_input.lower() == 'yes':
                disable_termination_protection(instance_id)
                instances_to_terminate.append(instance_id)
        else:
            instances_to_terminate.append(instance_id)
    
    if instances_to_terminate:
        response = ec2.terminate_instances(
            InstanceIds=instances_to_terminate
        )
        print("Termination response:", response)
    else:
        print("No instances to terminate.")

# Check and terminate instances
check_and_terminate(instance_ids)
