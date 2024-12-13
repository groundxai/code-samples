import os
import time
from groundx import GroundX, Document
from groundx.exceptions_base import OpenApiException
from dotenv import load_dotenv

load_dotenv()

if os.getenv("GROUNDX_API_KEY") is None:
    raise Exception("environment variable GROUNDX_API_KEY is not set")

opts = {
    "bucket_id": None,
    "file_type": "pdf",
    "file_name": "attention.pdf",
    "path_or_url": "/home/attention.pdf"
}

# initialize client
client = GroundX(api_key=os.getenv("GROUNDX_API_KEY"))

def usingBucket():
    if not opts["bucket_id"]:
        # list buckets
        try:
            bucket_response = client.buckets.list()
    
            if len(bucket_response.buckets) < 1:
                print(bucket_response.buckets)
                raise Exception("no results from buckets")
    
            return bucket_response.buckets[0].bucket_id
        except OpenApiException as e:
            print("Exception when calling BucketApi.list: %s\n" % e)

def ingest(bucket_id):
    # upload local documents to GroundX
    try:
        ingest = client.ingest(
                documents=[
                    Document(
                        bucket_id = bucket_id,
                        file_name = opts["file_name"],
                        file_type = opts["file_type"],
                        file_path = opts["path_or_url"]
                    ),
                ]
        )

        while (
                ingest.ingest.status != "complete"
                and ingest.ingest.status != "error"
                and ingest.ingest.status != "cancelled"
                ):
            time.sleep(3)
            ingest = client.documents.get_processing_status_by_id(process_id=ingest.ingest.process_id)
    except OpenApiException as e:
        print("Exception when calling DocumentApi.upload_local: %s\n" % e)

bucket_id = opts["bucket_id"]
if not bucket_id:
    bucket_id =  usingBucket()

if not (opts["path_or_url"] and opts["file_type"] and opts["file_name"]):
    raise Exception("path_or_url/file_type/file_name is not set")

ingest(bucket_id)

