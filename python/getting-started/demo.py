import os
import time
from groundx import GroundX, Document
from groundx.exceptions_base import OpenApiException
from dotenv import load_dotenv

load_dotenv()

if os.getenv("GROUNDX_API_KEY") is None:
    raise Exception("environemnt variable GROUNDX_API_KEY is not set")

opts = {
    "query": "Transformer",
    "bucket_id": None,
    "file_type": "pdf",
    "file_name": "attention.pdf",
    "local_file_path": "/home/attention.pdf",
    "remote_url": None
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

def ingest(bucket_id, file):
    # upload local documents to GroundX
    try:
        ingest = client.ingest(
                documents=[
                    Document(
                        bucket_id = bucket_id,
                        file_name = opts["file_name"],
                        file_type = opts["file_type"],
                        file_path = file
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

def search(bucket_id):
    # search
    try:
        content_response = client.search.content(id=bucket_id, query=opts["query"])
        if not content_response.search.text:
            print("search query did not have results")
        else:
            print(content_response.search.text)
    except OpenApiException as e:
        print("Exception when calling SearchApi.content: %s\n" % e)

bucket_id = opts["bucket_id"]
if not bucket_id:
    bucket_id =  usingBucket()

if opts["local_file_path"] and not (opts["file_type"] and opts["file_name"]):
    raise Exception("local filepath is set but file_type/file_name is not")
if opts["remote_url"] and not (opts["file_type"] and opts["file_name"]):
    raise Exception("remote url is set but file_type/file_name is not")

if opts["local_file_path"]:
    ingest(bucket_id, opts["local_file_path"])
if opts["remote_url"]:
    ingest(bucket_id, opts["remote_url"])
if opts["query"]:
    search(bucket_id)

