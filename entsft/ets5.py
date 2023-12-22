# ets5.py

import boto3
import json
from datetime import datetime, timedelta
# Identify the unused AMIs 
# List of regions to check (Add or remove regions as needed)
regions_to_check = ['ap-south-1', 'us-east-1']

def identify_unused_amis_in_region(region):
    result = {
        "result": "",
        "error_message": None,
        "passorfail": "Pass"  # Default to "Pass" unless unused AMIs are found
    }

    try:
        ec2 = boto3.client('ec2', region_name=region)

        # Describe all AMIs owned by yourself
        response = ec2.describe_images(Owners=['self'])

        ninty_days_ago = datetime.utcnow() - timedelta(days=90)

        unused_amis_found = False

        for ami in response['Images']:
            ami_id = ami['ImageId']
            creation_date = ami['CreationDate']

            # Convert creation_date to a datetime object
            creation_datetime = datetime.strptime(creation_date, "%Y-%m-%dT%H:%M:%S.%fZ")

            if creation_datetime < ninty_days_ago:
                result["result"] += f"<li>Identifying unused AMIs in region {region}...AMI {ami_id} was created more than 90 days ago and might be unused in region {region}.</li>"
                unused_amis_found = True

        if unused_amis_found:
            result["passorfail"] = "Fail"
        else:
            result["result"] += f"<ul><li>Identifying unused AMIs in region {region}...No unused AMIs found in region {region}.</li></ul>"

        return result

    except Exception as e:
        result["error_message"] = f"{type(e).__name__} at line {e.__traceback__.tb_lineno}: {e}"
        return result

def identify_unused_amis_in_all_regions():
    results = {"result": "", "error_message": None, "passorfail": "Pass"}
    
    for region in regions_to_check:
        region_result = identify_unused_amis_in_region(region)
        results["result"] += region_result["result"]

        if region_result["error_message"]:
            results["error_message"] = region_result["error_message"]
            results["passorfail"] = "Error"
        elif region_result["passorfail"] == "Fail":
            results["passorfail"] = "Fail"

    print(json.dumps(results, indent=4))

def main():
    identify_unused_amis_in_all_regions()

if __name__ == '__main__':
    main()
