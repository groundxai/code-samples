import os
import time
from groundx import GroundX, Document
from dotenv import load_dotenv

load_dotenv()

if os.getenv("GROUNDX_API_KEY") is None:
    raise Exception("You have not set a required environment variable (GROUNDX_API_KEY). Copy .env.sample and rename it to .env then fill in the missing values.")

opts = {
    "query": "YOUR QUERY",

    # set to a value to skip a bucket lookup
    # otherwise this demo will use the first result from get all buckets
    "bucket_id": None,

    # enumerated file type (e.g. docx, pdf)
    "file_type": "",
    "file_name": "",

    # remote url or local file path for ingest
    "path_or_url": ""
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
        except Exception as e:
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
    except Exception as e:
        print("Exception when calling DocumentApi.upload_local: %s\n" % e)

def search(bucket_id):
    # search
    try:
        content_response = client.search.content(id=bucket_id, query=opts["query"])
        if not content_response.search.text:
            print("search query did not have results")
        else:
            print(content_response.search.text)
    except Exception as e:
        print("Exception when calling SearchApi.content: %s\n" % e)

bucket_id = opts["bucket_id"]
if not bucket_id:
    bucket_id =  usingBucket()

if opts["path_or_url"] and not (opts["file_type"] and opts["file_name"]):
    raise Exception("path_or_url/file_type/file_name is nto set")

if opts["path_or_url"]:
    ingest(bucket_id)
if opts["query"]:
    search(bucket_id)

