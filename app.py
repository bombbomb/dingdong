import boto3
import pygame
import sys

client = boto3.client('sqs')

args = sys.argv

if len(args) == 1:
    print("You must pass in a queue_url")
    exit()

queue_url = args[1]

print("Connecting to Queue URL: " + queue_url)


def play_door_bell():
    pygame.mixer.init()
    pygame.mixer.music.load("doorbell.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

while True:
    get_resp = client.receive_message(
        QueueUrl=queue_url,
        VisibilityTimeout=30,
        WaitTimeSeconds=20
    )

    if 'Messages' in get_resp:
        msg = get_resp['Messages'][0]
        del_resp = client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=msg['ReceiptHandle']
        )
        play_door_bell()
    else:
        print("Nothing...")



