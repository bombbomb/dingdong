import boto3
import sys
import subprocess

args = sys.argv

if len(args) < 5:
    print("You must pass arguments in order: queue_url, aws key, aws secret, aws region")
    exit()

queue_url = args[1]
key = args[2]
secret = args[3]
region = args[4]

client = boto3.client(
    'sqs',
    aws_access_key_id=key,
    aws_secret_access_key=secret,
    region_name=region
)

print("Connecting to Queue URL: " + queue_url)

while True:
    get_resp = client.receive_message(
        QueueUrl=queue_url,
        WaitTimeSeconds=20
    )

    if 'Messages' in get_resp:
        msg = get_resp['Messages'][0]
        del_resp = client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=msg['ReceiptHandle']
        )
        print("Ding Dong!")
        subprocess.call(['aplay -fdat doorbell.wav'], shell=True)
