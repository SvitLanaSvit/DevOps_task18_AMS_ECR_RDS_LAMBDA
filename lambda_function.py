import os
import boto3

ec2 = boto3.client("ec2")

TAG_KEY = os.environ.get("TAG_KEY", "AutoStop")
TAG_VALUE = os.environ.get("TAG_VALUE", "true")

def lambda_handler(event, context):
    # знайти всі running інстанси з тегом TAG_KEY=TAG_VALUE
    filters = [
        {"Name": f"tag:{TAG_KEY}", "Values": [TAG_VALUE]},
        {"Name": "instance-state-name", "Values": ["running"]},
    ]
    ids, token = [], None
    while True:
        resp = ec2.describe_instances(Filters=filters, NextToken=token) if token else ec2.describe_instances(Filters=filters)
        for r in resp.get("Reservations", []):
            for i in r.get("Instances", []):
                ids.append(i["InstanceId"])
        token = resp.get("NextToken")
        if not token:
            break

    # зупинити знайдені
    if ids:
        ec2.stop_instances(InstanceIds=ids)

    return {"stopped": ids}
