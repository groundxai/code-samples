from groundx import Groundx, ApiException

groundxKey = "YOUR_GROUNDX_KEY"
query = "YOUR_QUERY"

# set to skip lookup, otherwise will be set to first result
bucketId = 0

# set to skip lookup, otherwise will be set to first result
projectId = 0

# enumerated file type (e.g. docx, pdf)
# must be set to upload local or hosted
# fileType = ""
fileType = ""

# must be set to upload local
fileName = ""

# set to local file path to upload local file
uploadLocal = ""

# set to hosted URL to upload hosted file
uploadHosted = ""

if groundxKey == "YOUR_GROUNDX_KEY":
    raise Exception("set your GroundX key")


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


if uploadLocal != "" and fileType != "" and fileName != "":
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


if uploadHosted != "" and fileType != "":
    # upload hosted documents to GroundX
    try:
        ingest = groundx.documents.upload_remote(
            documents=[
                {
                    "bucketId": bucketId,
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


if projectId == 0:
    # list projects
    try:
        project_response = groundx.projects.list()

        if len(project_response.body["projects"]) < 1:
            print(project_response.body["projects"])
            raise Exception("no results from projects")

        projectId = project_response.body["projects"][0]["projectId"]
        print(projectId)
    except ApiException as e:
        print("Exception when calling ProjectApi.list: %s\n" % e)


if query != "":
    # search
    try:
        content_response = groundx.search.content(id=projectId, search={"query": query})

        print(content_response.body["search"])
    except ApiException as e:
        print("Exception when calling SearchApi.content: %s\n" % e)
