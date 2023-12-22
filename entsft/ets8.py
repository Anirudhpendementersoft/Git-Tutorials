# ets8.py

import boto3
import json
# Ensure that EBS volumes are encrypted
# AWS credentials (ensure they are configured correctly)
# aws_access_key = 'YOUR_ACCESS_KEY'
# aws_secret_key = 'YOUR_SECRET_KEY'

# List of regions to check (Add or remove regions as needed)
regions_to_check = ['ap-south-1','us-east-2','us-east-1']

def check_ebs_volumes_encryption(region):
    result = {
        "result": "",
        "error_message": None,
        "passorfail": "Pass"
    }

    try:
        status_message = f"Checking EBS volumes for encryption status in region {region}....."
        result["result"] += f"<ul><li>{status_message}</li></ul>"
        # print(status_message)

        # Create an EC2 client for the specified region
        ec2_client = boto3.client('ec2', region_name=region)
        # ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region)

        # Describe all EBS volumes in the current region
        response = ec2_client.describe_volumes()

        volume_results = []
        volume_not_results = []
        for volume in response['Volumes']:
            volume_id = volume['VolumeId']
            encrypted = volume.get('Encrypted', False)

            if not encrypted:
                volume_not_results.append(f"<li>Volume {volume_id} is not encrypted in region {region}.</li>")
            else:
                volume_results.append(f"<li>Volume {volume_id} is encrypted in region {region}.</li>")

        if volume_results:
            result["result"] += f"<ul>{''.join(volume_results)}</ul>"
            result["passorfail"] = "Pass"
        elif volume_not_results:
            result["result"] += f"<ul>{''.join(volume_not_results)}</ul>"
            result["passorfail"] = "Fail"
        else:
            result["result"] += f"<ul><li>No volume are found in region {region}</li></ul>"


        # print(f"Encryption check completed for region {region}.\n")
        return result

    except Exception as e:
        result["error_message"] = f"{type(e).__name__} at line {e.__traceback__.tb_lineno}: {e}"
        return result

def check_ebs_volumes_encryption_in_all_regions():
    results = {"result": "", "error_message": None, "passorfail": "Pass"}
    for region in regions_to_check:
        region_result = check_ebs_volumes_encryption(region)

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
    check_ebs_volumes_encryption_in_all_regions()

if __name__ == '__main__':
    main()


