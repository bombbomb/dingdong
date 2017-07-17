import boto3
import sys
import pyglet

client = boto3.client('sqs')

args = sys.argv

if len(args) == 1:
    print("You must pass in a queue_url")
    exit()

queue_url = args[1]

print("Connecting to Queue URL: " + queue_url)

sound = pyglet.resource.media('doorbell.wav', streaming=False)

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
        sound.play()
