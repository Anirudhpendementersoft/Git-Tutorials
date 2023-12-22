# ets4.py

import boto3
import json
# Ensure  security group doesnot allow SSH ingress from 0.0.0.0/0
def check_security_groups(region):
    result = {
        "result": "",
        "error_message": None,
        "passorfail": "Pass"
    }

    try:
        ec2 = boto3.client('ec2', region_name=region)

        # Describe all security groups
        response = ec2.describe_security_groups()

        # print(f"Checking security groups for SSH ingress from 0.0.0.0/0 in region {region}...")

        insecure_security_groups = []

        for group in response['SecurityGroups']:
            group_id = group['GroupId']
            ingress_rules = group.get('IpPermissions', [])

            for rule in ingress_rules:
                from_port = rule.get('FromPort')
                to_port = rule.get('ToPort')

                if (
                    from_port is not None and to_port is not None and
                    rule.get('IpRanges', []) == [{'CidrIp': '0.0.0.0/0'}] and
                    from_port == 22 and to_port == 22
                ):
                    insecure_security_groups.append(f"<li>Security Group {group_id} allows SSH ingress from 0.0.0.0/0 in region {region}.</li>")

        if insecure_security_groups:
            result["result"] = f"<ul>{''.join(insecure_security_groups)}</ul>"
            result["passorfail"] = "Fail"
        else:
            result["result"] = f"<ul><li>All security groups in region {region} restrict SSH ingress from 0.0.0.0/0.</li></ul>"
            result["passorfail"] = "Pass"

        return result

    except Exception as e:
        result["error_message"] = f"{type(e).__name__} at line {e.__traceback__.tb_lineno}: {e}"
        return result

def check_security_groups_in_all_regions():
    results = {"result": "", "error_message": None, "passorfail": "Pass"}
    regions_to_test = ['us-east-2','ap-south-1']  # Add or remove regions as needed

    for region in regions_to_test:
        region_result = check_security_groups(region)

        # Combine results for all regions
        results["result"] += region_result["result"]

        # If an error occurred in any region, set the error message and passorfail accordingly
        if region_result["error_message"]:
            results["error_message"] = region_result["error_message"]
            results["passorfail"] = "Error"
        elif region_result["passorfail"] == "Fail":
            results["passorfail"] = "Fail"

    print(json.dumps(results, indent=4))

if __name__ == "__main__":
    check_security_groups_in_all_regions()


