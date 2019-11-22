import json
import boto3
import logging

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#define the connection
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
    filters = [{
            'Name': 'tag:madhav',
            'Values': ['YES','Yes','yes']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    
    #filter the instances
    instances = ec2.instances.filter(Filters=filters)

    #locate all running instances
    RunningInstances = [instance.id for instance in instances]
    
    #print the instances for logging purposes
    #print RunningInstances 
    
    #make sure there are actually instances to down bring them up. 
    if len(RunningInstances) > 0:
        #perform the shutdown
        ShuttingInstances = ec2.instances.filter(InstanceIds=RunningInstances).stop()
        print ShuttingInstances
        return {
            'statusCode': 200,
            'body': json.dumps(str(ShuttingInstances))
        }
    else:
        print "Nothing to see here"
        return {
            'statusCode': 200,
            'body': json.dumps("Nothing to see here")
        }

