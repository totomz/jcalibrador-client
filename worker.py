#!/usr/bin/python2.7 -p

import boto3
import json
import subprocess
from multiprocessing import Pool

# Create SQS client
sqs = boto3.client('sqs', region_name='us-east-2')

region = sqs._client_config.region_name

queue_jobs = 'https://%s.queue.amazonaws.com/242728094507/jcalibrador-jobs' % region
queue_results = 'https://%s.queue.amazonaws.com/242728094507/jcalibrador-results' % region


def get_jobs():

    messages = []

    print("Start polling")
    pool = Pool()

    while True:
        resp = sqs.receive_message(
            QueueUrl=queue_jobs,
            AttributeNames=['All'],
            MaxNumberOfMessages=1,
            VisibilityTimeout=120,
            WaitTimeSeconds=2
        )

        try:
            # Parse the body and fork a new process to run the command
            job = json.loads(resp['Messages'][0]['Body'])
            pool.apply_async(process_job, (job,))
        except KeyError:
            break


def process_job(job):
    out = subprocess.check_output(["docker", "run", job['image']] + job['args'].split(' '), stderr=subprocess.STDOUT)
    result = ''.join(out.splitlines())
    # Se qualcosa va in merda so cazzi
    response = sqs.send_message(
        QueueUrl=queue_results,
        MessageBody=json.dumps({'id': job['id'], 'result': float(result)})
    )
    print("ma ha mandato?")
    print(response)


get_jobs()
