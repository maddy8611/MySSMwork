import boto3
from datetime import datetime, date
import json
import xlsxwriter
import pprint
import os


def pp(item):
    pprint.pprint(item)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def instance_patch_info(client):
    pages = client.get_paginator('describe_instance_information')
    all_instances = []
    for page in pages.paginate():
        all_instances.extend(page.get("InstanceInformationList", []))
    json_serialized = json.loads(json.dumps(all_instances, default=json_serial))
    print(json_serialized)
    columns = []
    all_rows = []
    instance_ids =[]
    for each_instance in json_serialized:
        instance_ids.append(each_instance["InstanceId"])
        row = ["" for col in columns]
        for key, value in each_instance.items():
            try:
                index = columns.index(key)
            except ValueError:
                # this column hasn't been seen before
                columns.append(key)
                row.append("")
                index = len(columns) - 1
            row[index] = value
        all_rows.append(row)
    import csv
    with open("instances.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        # first row is the headers
        writer.writerow(columns)
        # then, the rows
        writer.writerows(all_rows)
    all_instance_response = {}
    for each_instance in instance_ids:
        paginator = client.get_paginator('describe_instance_patches')
        page_iterator = paginator.paginate(InstanceId=each_instance, PaginationConfig={'MaxItems': 100})
        items = []
        for each_page in page_iterator:
            try:
                print(each_page.get("Patches", []))
                items.extend(each_page.get("Patches", []))
            except Exception as err:
                print(each_page.get("Patches", []))
                pdb.set_trace()
        pdb.set_trace()
        for item in items:
            pass
        all_instances = []

        response = client.describe_instance_patches(
            InstanceId=each_instance
        )
        pdb.set_trace()
      #  for each_patch in response["Patches"]:
      #      header_rows.extend(list(each_patch.keys()))

        all_instance_response[each_instance] = response["Patches"]

        row = 0
        column = 0
        headers = list(set(header_rows))
        # To Make sure the first Cell has the instance ID
        patch_worksheet.write(row, column, "InstanceID")
        column += 1
        for each_header in headers:
            patch_worksheet.write(row, column, each_header)
            column += 1

        row = 1
        column = 1
        for each_instance in all_instance_response:
            print(each_instance)
            for each_patch in all_instance_response[each_instance]:
                patch_worksheet.write(row, 0, each_instance)
                for each_header in headers:
                    cell_value = each_patch.get(each_header, "None")
                    if type(cell_value) not in [int, str, float, bool]:
                        cell_value = str(cell_value)
                    patch_worksheet.write(row, column, cell_value)
                    column += 1
                column = 1
                row += 1
        workbook.close()
        return outfile



def upload_file_s3(client, bucket_name, to_be_upload_filename):
    only_filename = os.path.basename(to_be_upload_filename)

    try:
        return client.upload_file(to_be_upload_filename, bucket_name, only_filename)
    except Exception as err:
        return err

def lambda_handler(event, context):
    client = boto3.client('ssm', region_name="us-east-1")
    filename = instance_patch_info(client)
    print(filename)
    s3_client = boto3.client("s3",region_name="us-east-1")
    bucket_name = '2ftv-ssm-logs-42212-s3'
    #return upload_file_s3(s3_client, bucket_name, filename)



if __name__ == "__main__":
    import pdb
    pdb.set_trace()
    pprint.pprint(lambda_handler({}, {}))


