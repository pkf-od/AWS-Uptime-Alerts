import boto3
import time
import os

def lambda_handler(event, context):
    
    # Get the VM Instance's ID
    instance_id = os.environ['INSTANCE_ID']
    #print(f"Instance ID: {instance_id}")
    
    # Create an ec2 client to programmatically interact with the EC2 instance
    ec2_client = boto3.client('ec2')
    
    # Get information about the EC2 instance using it's instance ID
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    
    # Get the launch time of the VM instance from the JSON response
    launch_time = response['Reservations'][0]['Instances'][0]['LaunchTime']
    #print(f"Launch Time: {launch_time}")
    
    # Get the current time of when program is executed
    current_time = time.time()
    #print(f"Current Time: {current_time}")

    # Subtract the launch time from the current time to determine has much time has elapsed
    uptime = current_time - launch_time.timestamp()
    #print(f"Uptime in seconds: {uptime}")
    
    # Convert the uptime to hours for display
    uptime_in_hours = uptime / 3600
    #print(f"Uptime in hours: {uptime_in_hours}")
    
    # Check if the VM instance is currently running
    instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
    print(f"Instance State: {instance_state}")
    
    # We only want to send an email if the VM instance is running AND the uptime > 2 hours
    if instance_state == "running":
        # If uptime is greater than 7200 seconds (or 2 hours), then we want to issue an alert
        if uptime > 7200:
            sns_client = boto3.client('sns')
            sns_topic_arn = os.environ['SNS_TOPIC_ARN']
            sns_client.publish(
                TopicArn=sns_topic_arn,
                Message='C2/Nessus/Burp VM instance {} has exceeded 2 hours of uptime, with a total uptime of {:.02f} hours.'.format(instance_id, uptime_in_hours)
            )
            print("Uptime Threshold Exceeded, emails will be sent!")
        else:
            print("Uptime Threshold Not Exceeded, no emails will be sent.")
    else:
        print("VM Instance is currently stopped.")