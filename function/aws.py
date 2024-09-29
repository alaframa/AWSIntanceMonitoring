import boto3
import json
import os


# Function to load AWS config from the config file
def load_aws_config():
    config_file_path = os.path.join(os.path.dirname(__file__), '../config/aws_config.json')
    
    try:
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        print("Config file not found.")
        return None
    except json.JSONDecodeError:
        print("Error parsing the config file.")
        return None

aws_config = load_aws_config()
# Create an EC2 client

ec2 = boto3.client(
    'ec2',
    aws_access_key_id=aws_config['aws_access_key_id'],
    aws_secret_access_key=aws_config['aws_secret_access_key'],
    region_name=aws_config['region_name']
)

def getAwsData():
    try:
        response = ec2.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_state = instance['State']['Name']
                private_ip = instance.get('PrivateIpAddress')
                public_ip = instance.get('PublicIpAddress', 'No Public IP')
                instance_data = {
                    'State': instance_state,
                    'Instance ID': instance_id,
                    'Private IP': private_ip,
                    'Public IP': public_ip
                }
                instances.append(instance_data)
        return instances
    except Exception as e:
        print(f"Error listing instances: {e}")
        return []

def startAWS(instanceID):
    try:
        ec2.start_instances(InstanceIds=[instanceID])
    except Exception as e:
        print (e)

def stopAWS(instanceID):
    try:
        ec2.stop_instances(InstanceIds=[instanceID])        
    except Exception as e:
        print (e)


