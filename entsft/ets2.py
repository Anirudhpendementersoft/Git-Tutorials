# ets2.py

import boto3
import json
# Ensure VPC restricts traffic
# AWS credentials (ensure they are configured correctly)
aws_access_key = 'AKIA4NOIYUP7KVOKHVE6'
aws_secret_key = '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'

# List of regions to check (Add or remove regions as needed)
regions_to_check = ['us-east-2', 'ap-south-1']

def check_default_security_groups_in_region(region):
    result = {
        "result": "",
        "error_message": None,
        "passorfail": "Pass"
    }

    try:
        # Create an EC2 client for the specified region
        ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region)

        # Get a list of all VPCs in the account for the specified region
        vpcs = ec2_client.describe_vpcs()['Vpcs']

        # Check the default security group of each VPC
        default_sg_results = []
        restrict_default_sg_results = []
        for vpc in vpcs:
            vpc_id = vpc['VpcId']
            default_sg = ec2_client.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}, {'Name': 'group-name', 'Values': ['default']}])['SecurityGroups'][0]
            
            inbound_rules = default_sg.get('IpPermissions', [])
            outbound_rules = default_sg.get('IpPermissionsEgress', [])

            if inbound_rules or outbound_rules:
                default_sg_results.append(f"<li>Default security group of VPC {vpc_id} in region {region} allows traffic. Please review and restrict if necessary.</li>")
            else:
                restrict_default_sg_results.append(f"<li>Default security group of VPC {vpc_id} in region {region} restricts the traffic.</li>")

        if default_sg_results or restrict_default_sg_results:
            result["result"] = f"<ul>{''.join(default_sg_results + restrict_default_sg_results)}</ul>"
            result["passorfail"] = "Fail" if default_sg_results else "Pass"
        
        else:
            result["result"] = f"<ul><li>All default security groups in region {region} restrict traffic.</li></ul>"
            result["passorfail"] = "Pass"

        return result

    except Exception as e:
        result["error_message"] = f"{type(e).__name__} at line {e.__traceback__.tb_lineno}: {e}"
        return result

def check_default_security_groups_in_all_regions():
    results = {"result": "", "error_message": None, "passorfail": "Pass"}
    for region in regions_to_check:
        region_result = check_default_security_groups_in_region(region)

        # Append the result for the current region
        results["result"] += region_result["result"]

        # If an error occurred in any region, set the error message and passorfail accordingly
        if region_result["error_message"]:
            results["error_message"] = region_result["error_message"]
            results["passorfail"] = "Error"
        elif region_result["passorfail"] == "Fail":
            results["passorfail"] = "Fail"

    # Print the combined results
    if results["result"]:
        print(json.dumps(results, indent=4))

def main():
    check_default_security_groups_in_all_regions()

if __name__ == '__main__':
    main()

