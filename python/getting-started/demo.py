import asyncio
from groundx import Groundx, ApiException


# initialize client
groundx = Groundx(
    api_key="<your_api_key>",
)


# list buckets
try:
    bucket_response = groundx.bucket.list()

    print(bucket_response.body["buckets"])
except ApiException as e:
    print("Exception when calling BucketApi.list: %s\n" % e)


# upload local documents to GroundX
try:
    upload_local_response = groundx.document.upload_local(
        blob=[open("/path/to/your/file", "rb")],
        metadata={
            "bucket_id": <your_bucket_id>,
            "file_name": "my_file.pdf",
            "file_type": "pdf",
        },
    )
    print(upload_remote_response.body["ingest"])
except ApiException as e:
    print("Exception when calling DocumentApi.upload_local: %s\n" % e)


# upload hosted documents to GroundX
try:
    upload_remote_response = groundx.document.upload_remote(
        documents=[
            {
                "bucket_id": <your_bucket_id>,
                "source_url": "https://path.to.your/file.docx",
                "type": "docx",
            }
        ],
    )
    print(upload_remote_response.body["ingest"])
except ApiException as e:
    print("Exception when calling DocumentApi.upload_remote: %s\n" % e)


# check upload status
try:
    get_processing_status_by_id_response = groundx.document.get_processing_status_by_id(
        process_id="<processId>",  # required
    )
    print(get_processing_status_by_id_response.body["ingest"])
except ApiException as e:
    print("Exception when calling DocumentApi.get_processing_status_by_id: %s\n" % e)


# search when upload is complete
try:
    content_response = groundx.search.content(
        id=<id>,  # required
        search={"query": "<your_query>"}
    )
    print(content_response.body["search"])
except ApiException as e:
    print("Exception when calling SearchApi.content: %s\n" % e)


# list projects
try:
    project_response = groundx.project.list()
    print(project_response.body["projects"])
except ApiException as e:
    print("Exception when calling ProjectApi.list: %s\n" % e)
