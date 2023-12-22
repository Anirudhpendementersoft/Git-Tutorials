# ets10.py

import boto3
import json
# Check whether the versioning is enabled or not
# List of regions to check (Add or remove regions as needed)
regions_to_check = ['ap-south-1', 'us-east-2']

def check_all_bucket_versioning_in_region(region):
    result = {
        "result": "",
        "error_message": None,
        "passorfail": "Pass"
    }

    try:
        s3_client = boto3.client('s3', region_name=region)
        response = s3_client.list_buckets()

        result["result"] += f"<ul><li>Checking versioning status for all S3 buckets in region {region}...</li></ul>"

        for bucket in response['Buckets']:
            bucket_name = bucket['Name']

            try:
                versioning_response = s3_client.get_bucket_versioning(Bucket=bucket_name)
                status = versioning_response.get('Status', 'NotEnabled')

                if status == 'Enabled':
                    result["result"] += f"<li>Versioning is enabled for bucket {bucket_name} in region {region}.</li>"
                    result["passorfail"] = "Pass"
                else:
                    result["result"] += f"<li>Versioning is not enabled for bucket {bucket_name} in region {region}.</li>"
                    result["passorfail"] = "Fail"

            except s3_client.exceptions.NoSuchBucketVersioning:
                result["result"] += f"<li>Versioning is not enabled for bucket {bucket_name} in region {region}.</li>"

        return result

    except Exception as e:
        result["error_message"] = f"{type(e).__name__} at line {e.__traceback__.tb_lineno}: {e}"
        return result

def check_all_bucket_versioning_in_all_regions():
    results = {"result": "", "error_message": None, "passorfail": "Pass"}
    
    for region in regions_to_check:
        region_result = check_all_bucket_versioning_in_region(region)
        results["result"] += region_result["result"]

        if region_result["error_message"]:
            results["error_message"] = region_result["error_message"]
            results["passorfail"] = "Error"
        elif region_result["passorfail"] == "Fail":
            results["passorfail"] = "Fail"

    print(json.dumps(results, indent=4))

def main():
    check_all_bucket_versioning_in_all_regions()

if __name__ == '__main__':
    main()

