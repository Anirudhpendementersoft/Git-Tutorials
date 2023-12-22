# ets3.py

import boto3
import json
#  Ensure that termination protection is enabled
# AWS credentials (ensure they are configured correctly)
aws_access_key = 'AKIA4NOIYUP7KVOKHVE6'
aws_secret_key = '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'

# List of regions to check (Add or remove regions as needed)
regions_to_check = ['us-east-2', 'us-west-2']

def check_termination_protection_in_region(region):
    result = {
        "result": "",
        "error_message": None,
        "passorfail": "Pass"
    }

    try:
        # Create an EC2 client for the specified region
        ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region)

        # Get a list of all EC2 instances in the account for the specified region
        instances = ec2_client.describe_instances()['Reservations']

        # Check termination protection status for each instance
        termination_protection_results = []
        termination_not_protection_results = []
        for reservation in instances:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                
                # Describe instance attribute to check termination protection
                response = ec2_client.describe_instance_attribute(
                    InstanceId=instance_id,
                    Attribute='disableApiTermination'
                )

                termination_protection_enabled = response['DisableApiTermination']['Value']

                if termination_protection_enabled:
                    termination_protection_results.append(f"<li>Termination protection is enabled for EC2 instance {instance_id} in region {region}.</li>")
                else:
                    termination_not_protection_results.append(f"<li>Termination protection is not enabled for EC2 instance {instance_id} in region {region}.</li>")

        if termination_protection_results or termination_not_protection_results:
            result["result"] = f"<ul>{''.join(termination_protection_results + termination_not_protection_results)}</ul>"
            result["passorfail"] = "Fail" if termination_not_protection_results else "Pass"
        else:
            result["result"] = f"<ul><li>No EC2 instances are found in region {region}.</li></ul>"
            result["passorfail"] = "Pass"

        return result

    except Exception as e:
        result["error_message"] = f"{type(e).__name__} at line {e.__traceback__.tb_lineno}: {e}"
        return result

def check_termination_protection_in_all_regions():
    results = {"result": "", "error_message": None, "passorfail": "Pass"}
    for region in regions_to_check:
        region_result = check_termination_protection_in_region(region)

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
    check_termination_protection_in_all_regions()

if __name__ == '__main__':
    main()


