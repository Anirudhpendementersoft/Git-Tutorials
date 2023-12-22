# ets1.py

import boto3
import json
# Ensure that AMIs are encrypted
# AWS credentials (ensure they are configured correctly)
aws_access_key = 'AKIA4NOIYUP7KVOKHVE6'
aws_secret_key = '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'

# List of regions to check (Add or remove regions as needed)
regions_to_check = ['ap-south-1', 'us-east-2']

def check_ami_encryption_in_region(region):
    result = {
        "result": "",
        "error_message": None,
        "passorfail": "Pass"
    }

    try:
        # Create an EC2 client for the specified region
        ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region)

        # Get a list of all AMIs in the account for the specified region
        amis = ec2_client.describe_images(Owners=['self'])['Images']

        # Check the encryption status of each AMI
        ami_encryption_status = []
        ami_not_encryption_status = []
        for ami in amis:
            ami_id = ami['ImageId']
            encryption_status = ami.get('BlockDeviceMappings', [{}])[0].get('Ebs', {}).get('Encrypted', False)

            if encryption_status:
                ami_encryption_status.append(f"<li>AMI {ami_id} in region {region} is encrypted.</li>")
            else:
                ami_not_encryption_status.append(f"<li>AMI {ami_id} in region {region} is not encrypted.</li>")

        if ami_encryption_status:
            result["result"] = f"<ul>{''.join(ami_encryption_status)}</ul>"
            result["passorfail"] = "Pass"

        elif ami_not_encryption_status:
            result["result"] = f"<ul>{''.join(ami_not_encryption_status)}</ul>"
            result["passorfail"] = "Fail"
        else:
            result["result"] = f"<ul><li>No AMIs are found in region {region}.</li></ul>"
            result["passorfail"] = "Pass"

        return result

    except Exception as e:
        result["error_message"] = f"{type(e).__name__} at line {e.__traceback__.tb_lineno}: {e}"
        return result

def check_ami_encryption_in_all_regions():
    results = {"result": "", "error_message": None, "passorfail": "Pass"}
    for region in regions_to_check:
        region_result = check_ami_encryption_in_region(region)

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
    check_ami_encryption_in_all_regions()

if __name__ == '__main__':
    main()


