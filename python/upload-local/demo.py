from groundx import Groundx, ApiException

groundxKey = "YOUR_GROUNDX_KEY"

# set to skip lookup, otherwise will be set to first result
bucketId = 0

# enumerated file type (e.g. docx, pdf)
# must be set to upload local or hosted
# fileType = ""
fileType = ""

# must be set to upload local
fileName = ""

# set to local file path to upload local file
uploadLocal = ""

if groundxKey == "YOUR_GROUNDX_KEY":
    raise Exception("set your GroundX key")

if uploadLocal == "":
    raise Exception("set the local file path")

if fileType == "":
    raise Exception("set the file type to a supported enumerated type (e.g. txt, pdf)")

if fileName == "":
    raise Exception("set a name for the file")


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


# upload local documents to GroundX
try:
    ingest = groundx.documents.upload_local(
        body=[
            {
                "blob": open(uploadLocal, "rb"),
                "metadata": {
                    "bucketId": bucketId,
                    "fileName": fileName,
                    "fileType": fileType,
                    # optional metadata field
                    # content is added to document chunks
                    # fields are search during search requests
                    # and returned in search results
                    "metadata": {"key": "value"},
                },
            },
        ]
    )

    while (
        ingest.body["ingest"]["status"] != "complete"
        and ingest.body["ingest"]["status"] != "error"
    ):
        ingest = groundx.documents.get_processing_status_by_id(
            process_id=ingest.body["ingest"]["processId"]
        )
except ApiException as e:
    print("Exception when calling DocumentApi.upload_local: %s\n" % e)
