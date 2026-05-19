#!/usr/bin/env python3
"""
AWS EC2 Resource Tagger – adds a common tag to all instances in a region.
Prerequisites: pip install boto3, AWS credentials configured
Usage: python cloud_tagger.py --region us-east-1 --tag Environment=Production
"""

import argparse
import sys
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def tag_instances(region, tag_key, tag_value):
    try:
        ec2 = boto3.client("ec2", region_name=region)
        paginator = ec2.get_paginator("describe_instances")
        instance_ids = []
        for page in paginator.paginate():
            for reservation in page["Reservations"]:
                for instance in reservation["Instances"]:
                    instance_ids.append(instance["InstanceId"])

        if not instance_ids:
            print("No instances found.")
            return

        print(f"Tagging {len(instance_ids)} instances with {tag_key}={tag_value}...")
        ec2.create_tags(Resources=instance_ids, Tags=[{"Key": tag_key, "Value": tag_value}])
        print("Done.")
    except (BotoCoreError, ClientError) as e:
        print(f"AWS error: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Tag EC2 instances")
    parser.add_argument("--region", required=True, help="AWS region")
    parser.add_argument("--tag", required=True, help="Key=Value pair")
    args = parser.parse_args()
    key, value = args.tag.split("=", 1)
    tag_instances(args.region, key, value)

if __name__ == "__main__":
    main()