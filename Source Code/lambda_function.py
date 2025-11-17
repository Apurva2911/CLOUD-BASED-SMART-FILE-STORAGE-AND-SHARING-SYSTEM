import json
import boto3
import os
import base64
import jwt
import uuid
from datetime import datetime, timedelta

# AWS Clients
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

# Environment Variables
BUCKET_NAME = os.environ.get("bucket_name", "drive-files-project1")
TABLE_NAME = os.environ.get("table_name", "SmartDriveFiles")

# DynamoDB Table
table = dynamodb.Table(TABLE_NAME)

# JWT Secret
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "37cf4a883d379c8c6430dce285984af89dd78cedc15f191368ca9f0f2c8da43a"
)

# Response helper
def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST,DELETE",
            "Access-Control-Allow-Headers": "Content-Type,Authorization"
        },
        "body": json.dumps(body)
    }

def verify_jwt(headers):
    token = headers.get("Authorization", "").replace("Bearer ", "")
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return decoded["email"]

def lambda_handler(event, context):
    print("EVENT:", json.dumps(event))
    path = event.get("path", "")
    method = event.get("httpMethod", "")

    if method == "OPTIONS":
        return response(200, {"message": "CORS OK"})

    # ------------------------- LOGIN -------------------------
    if path == "/login" and method == "POST":
        body = json.loads(event.get("body", "{}"))
        username = body.get("username")
        password = body.get("password")

        if username == "Apurva kadam" and password == "Apurva@123":
            token = jwt.encode(
                {"email": "apurvak2911@gmail.com", "exp": datetime.utcnow() + timedelta(hours=1)},
                SECRET_KEY,
                algorithm="HS256"
            )
            return response(200, {"token": token})
        else:
            return response(401, {"error": "Invalid credentials"})

    # ------------------------- UPLOAD -------------------------
    if path == "/upload" and method == "POST":
        try:
            email = verify_jwt(event.get("headers", {}))
            body = json.loads(event.get("body", "{}"))
            filename = body.get("filename")
            file_content = base64.b64decode(body.get("fileContent", ""))

            # Upload to S3
            s3.put_object(Bucket=BUCKET_NAME, Key=filename, Body=file_content)

            # Generate UUID file_id
            file_id = str(uuid.uuid4())

            # Add metadata to DynamoDB
            table.put_item(
                Item={
                    "file_id": file_id,
                    "file_name": filename,
                    "owner_email": email,
                    "upload_date": datetime.utcnow().isoformat()
                }
            )

            return response(200, {"message": f"File '{filename}' uploaded!", "file_id": file_id})
        except Exception as e:
            print("Upload error:", e)
            return response(500, {"error": str(e)})

    # ------------------------- LIST FILES -------------------------
    if path == "/files" and method == "GET":
        try:
            email = verify_jwt(event.get("headers", {}))

            res = table.scan(
                FilterExpression="owner_email = :e",
                ExpressionAttributeValues={":e": email}
            )

            return response(200, {"files": res.get("Items", [])})
        except Exception as e:
            print("List error:", e)
            return response(500, {"error": str(e)})

    # ------------------------- DELETE FILE -------------------------
    if path == "/delete" and method == "DELETE":
        try:
            email = verify_jwt(event.get("headers", {}))
            body = json.loads(event.get("body", "{}"))
            file_id = body.get("file_id")

            item = table.get_item(Key={"file_id": file_id}).get("Item")
            if not item or item["owner_email"] != email:
                return response(403, {"error": "You cannot delete this file"})

            s3.delete_object(Bucket=BUCKET_NAME, Key=item["file_name"])
            table.delete_item(Key={"file_id": file_id})

            return response(200, {"message": "File deleted!"})
        except Exception as e:
            print("Delete error:", e)
            return response(500, {"error": str(e)})

    # ------------------------- DOWNLOAD -------------------------
    if path == "/download" and method == "GET":
        try:
            email = verify_jwt(event.get("headers", {}))
            params = event.get("queryStringParameters") or {}
            filename = params.get("filename")

            # Optional: verify ownership
            res = table.scan(
                FilterExpression="file_name = :f AND owner_email = :e",
                ExpressionAttributeValues={":f": filename, ":e": email}
            )
            if not res.get("Items"):
                return response(403, {"error": "You cannot download this file"})

            file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=filename)
            file_content = base64.b64encode(file_obj["Body"].read()).decode("utf-8")

            return response(200, {"filename": filename, "fileContent": file_content})
        except Exception as e:
            print("Download error:", e)
            return response(500, {"error": str(e)})

    # ------------------------- SHARE (Presigned URL) -------------------------
    if path == "/share" and method == "POST":
        try:
            email = verify_jwt(event.get("headers", {}))
            body = json.loads(event.get("body", "{}"))
            file_id = body.get("file_id")

            item = table.get_item(Key={"file_id": file_id}).get("Item")
            if not item or item["owner_email"] != email:
                return response(403, {"error": "You cannot share this file"})

            filename = item["file_name"]
            url = s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": BUCKET_NAME, "Key": filename},
                ExpiresIn=3600
            )

            return response(200, {"shareable_link": url})
        except Exception as e:
            print("Share error:", e)
            return response(500, {"error": str(e)})

    return response(404, {"error": "Route not found"})
