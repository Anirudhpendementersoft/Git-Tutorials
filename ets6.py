# ets6.py

import boto3
import json
# Identify unused keypairs
# AWS credentials (ensure they are configured correctly)
# aws_access_key = 'YOUR_ACCESS_KEY'
# aws_secret_key = 'YOUR_SECRET_KEY'

# List of regions to check (Add or remove regions as needed)
regions_to_check = ['ap-south-1', 'us-east-1']

def display_unused_key_pairs(region):
    result = {
        "result": "",
        "error_message": None,
        "passorfail": "Pass"
    }

    try:
        # Create an EC2 client for the specified region
        ec2_client = boto3.client('ec2', region_name=region)
        # ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region)

        # Describe all key pairs
        key_pairs_response = ec2_client.describe_key_pairs()
        key_pairs = {kp['KeyName']: kp for kp in key_pairs_response['KeyPairs']}

        # Describe all instances
        instances_response = ec2_client.describe_instances()
        instances = [instance for reservation in instances_response['Reservations'] for instance in reservation['Instances']]

        status_message = f"Displaying unused key pairs in region {region}..."
        result["result"] += f"<ul><li>{status_message}</li></ul>"
        # print(status_message)

        unused_key_pairs = []
        for key_pair_name, key_pair in key_pairs.items():
            # Check if the key pair is associated with any instances
            is_associated = any(key_pair_name == instance['KeyName'] for instance in instances)

            if not is_associated:
                unused_key_pairs.append(f"<li>Key pair {key_pair_name} is not associated with any running instances.</li>")
            else:
                unused_key_pairs.append(f"<li>Key pair {key_pair_name} is associated with running instances.</li>")

        if unused_key_pairs:
            result["result"] += f"<ul>{''.join(unused_key_pairs)}</ul>"
            result["passorfail"] = "Fail"
        else:
            result["result"] += f"<ul><li>No unused key pairs found in region {region}.</li></ul>"
            result["passorfail"] = "Pass"

        return result

    except Exception as e:
        result["error_message"] = f"{type(e).__name__} at line {e.__traceback__.tb_lineno}: {e}"
        return result

def display_unused_key_pairs_in_all_regions():
    results = {"result": "", "error_message": None, "passorfail": "Pass"}
    for region in regions_to_check:
        region_result = display_unused_key_pairs(region)

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
    display_unused_key_pairs_in_all_regions()

if __name__ == '__main__':
    main()
