# ets9.py

import boto3
import json
# Ensure EBS snapshots are encrypted
# AWS credentials (ensure they are configured correctly)
# aws_access_key = 'YOUR_ACCESS_KEY'
# aws_secret_key = 'YOUR_SECRET_KEY'

# List of regions to check (Add or remove regions as needed)
regions_to_check = ['ap-south-1', 'us-east-2']

def check_ebs_snapshots_encryption(region):
    result = {
        "result": "",
        "error_message": None,
        "passorfail": "Pass"
    }

    try:
        # print(f"\nChecking EBS snapshots for encryption status in region {region}...")

        # Create an EC2 client for the specified region
        ec2 = boto3.client('ec2', region_name=region)
        # ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region)

        # Describe all EBS snapshots in the current region
        response = ec2.describe_snapshots(OwnerIds=['self'])

        status_message = f"Checking EBS snapshots for encryption status in region {region}......"
        result["result"] += f"<ul><li>{status_message}</li></ul>"
        # print(status_message)

        snapshot_results = []
        snapshot_not_results = []

        for snapshot in response['Snapshots']:
            snapshot_id = snapshot['SnapshotId']
            encrypted = snapshot.get('Encrypted', False)

            if not encrypted:
                snapshot_not_results.append(f"<li>Snapshot {snapshot_id} is not encrypted.</li>")
            else:
                snapshot_results.append(f"<li>Snapshot {snapshot_id} is encrypted.</li>")

        if snapshot_results:
            result["result"] += f"<ul>{''.join(snapshot_results)}</ul>"
            result["passorfail"] = "Pass"
        elif snapshot_not_results:
            result["result"] += f"<ul>{''.join(snapshot_not_results)}</ul>"
            result["passorfail"] = "Fail"
        else:
            result["result"] += f"<ul><li>No snapshot are found in region {region}</li></ul>"

        return result

    except Exception as e:
        result["error_message"] = f"{type(e).__name__} at line {e.__traceback__.tb_lineno}: {e}"
        return result

def check_ebs_snapshots_encryption_in_all_regions():
    results = {"result": "", "error_message": None, "passorfail": "Pass"}
    for region in regions_to_check:
        region_result = check_ebs_snapshots_encryption(region)
        # region_result = check_ebs_snapshots_encryption(region, aws_access_key, aws_secret_key)

        # Combine results for all regions
        results["result"] += region_result["result"]

        # If an error occurred in any region, set the error message and passorfail accordingly
        if region_result["error_message"]:
            results["error_message"] = region_result["error_message"]
            results["passorfail"] = "Error"
        elif region_result["passorfail"] == "Fail":
            results["passorfail"] = "Fail"

    print(json.dumps(results, indent=4))

def main():
    check_ebs_snapshots_encryption_in_all_regions()

if __name__ == '__main__':
    main()

