from groundx import Groundx, ApiException

groundxKey = "YOUR_GROUNDX_KEY"

# set to skip lookup, otherwise will be set to first result
bucketId = 0

# enumerated file type (e.g. docx, pdf)
# must be set to upload local or hosted
# fileType = ""
fileType = ""

# set to hosted URL to upload hosted file
uploadHosted = ""

if groundxKey == "YOUR_GROUNDX_KEY":
    raise Exception("set your GroundX key")

if uploadHosted == "":
    raise Exception("set the hosted file URL")

if fileType == "":
    raise Exception("set the file type to a supported enumerated type (e.g. txt, pdf)")


# initialize client
groundx = Groundx(
    api_key=groundxKey,
)


if bucketId == 0:
    # list buckets
    try:
        bucket_response = groundx.buckets.list()

        if len(bucket_response.body["buckets"]) < 1:
            print(bucket_response.body["buckets"])
            raise Exception("no results from buckets")

        bucketId = bucket_response.body["buckets"][0]["bucketId"]
    except ApiException as e:
        print("Exception when calling BucketApi.list: %s\n" % e)


# upload hosted documents to GroundX
try:
    ingest = groundx.documents.upload_remote(
        documents=[
            {
                "bucketId": bucketId,
                # optional metadata field
                # content is added to document chunks
                # fields are search during search requests
                # and returned in search results
                "metadata": {"key": "value"},
                "sourceUrl": uploadHosted,
                "fileType": fileType,
            }
        ],
    )

    while (
        ingest.body["ingest"]["status"] != "complete"
        and ingest.body["ingest"]["status"] != "error"
    ):
        ingest = groundx.documents.get_processing_status_by_id(
            process_id=ingest.body["ingest"]["processId"]
        )
except ApiException as e:
    print("Exception when calling DocumentApi.upload_remote: %s\n" % e)
