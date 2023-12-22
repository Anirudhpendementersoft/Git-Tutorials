# ets.py

import boto3
import json
# Ensure that security group doesnot allow restricated inbound access
# AWS credentials (ensure they are configured correctly)
aws_access_key = 'AKIA4NOIYUP7KVOKHVE6'
aws_secret_key = '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'

# List of regions to check (Add or remove regions as needed)
# regions_to_check = ['us-east-2', 'ap-south-1']
regions_to_check =['us-east-2', 'us-west-2']

def check_security_groups_in_region(region):
    result = {
        "result": "",
        "error_message": None,
        "passorfail": "Pass"
    }

    try:
        # Create an EC2 client for the specified region
        ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region)

        # Get a list of all security groups in the account for the specified region
        security_groups = ec2_client.describe_security_groups()['SecurityGroups']

        # Check the inbound rules of each security group
        insecure_security_groups = []
        secure_security_groups = []
        for sg in security_groups:
            sg_id = sg['GroupId']
            inbound_rules = sg.get('IpPermissions', [])

            for rule in inbound_rules:
                if rule['IpRanges'] == [{'CidrIp': '0.0.0.0/0'}]:
                    secure_security_groups.append(f"<li>Security Group {sg_id} in region {region} allows unrestricted inbound access.</li>")
            else:
                insecure_security_groups.append(f"<li>Security Group {sg_id} in region {region} does not allow unrestricted inbound access.</li>")

        if insecure_security_groups:
            result["result"] = f"<ul>{''.join(insecure_security_groups)}</ul>"
            result["passorfail"] = "Pass"
        else:
            result["result"] = f"<ul>{''.join(insecure_security_groups)}</ul>"
            result["passorfail"] = "Fail"

        return result

    except Exception as e:
        result["error_message"] = f"{type(e).__name__} at line {e.__traceback__.tb_lineno}: {e}"
        return result

def check_security_groups_in_all_regions():
    results = {"result": "", "error_message": None, "passorfail": "Pass"}
    for region in regions_to_check:
        region_result = check_security_groups_in_region(region)
        
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
    check_security_groups_in_all_regions()

if __name__ == '__main__':
    main()



