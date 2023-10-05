import { Groundx } from "groundx-typescript-sdk";


// initialize client
const groundx = new Groundx({
  apiKey: "<your_api_key>",
});


// list buckets
const bucketResponse = await groundx.bucket.list();
console.log(bucketResponse);


// upload local documents to GroundX
const uploadLocalResponse = await groundx.document.uploadLocal({
  blob: [open("/path/to/your/file", "rb")],
  metadata: {
    bucketId: <your_bucket_id>,
    fileName: "my_file.pdf",
    fileType: "pdf"
  },
});
console.log(uploadLocalResponse);


// upload hosted documents to GroundX
const uploadRemoteResponse = await groundx.document.uploadRemote({
  bucketId: <your_bucket_id>,
  sourceUrl: "https://path.to.your/file.docx",
  type: "docx"
});
console.log(uploadRemoteResponse);


// check upload status
const getProcessingStatusByIdResponse =
await groundx.document.getProcessingStatusById({
  processId: "<processId>",
});
console.log(getProcessingStatusByIdResponse);


// search when upload is complete
const contentResponse = await groundx.search.content({
  id: <id>,
  search: {
    query: "<your_query>"
  },
});
console.log(contentResponse);

// list projects
const projResponse = await groundx.project.list();
console.log(projResponse);