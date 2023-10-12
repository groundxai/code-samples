import fs from 'fs';
import { Groundx } from "groundx-typescript-sdk";

const groundxKey = "YOUR_GROUNDX_KEY";
const query = "YOUR_QUERY";

// set to skip lookup, otherwise will be set to first result
let bucketId = 0;

// set to skip lookup, otherwise will be set to first result
let projectId = 0;

// enumerated file type (e.g. docx, pdf)
// must be set to upload local or hosted
const fileType = "";

// must be set to upload local
const fileName = ""

// set to local file path to upload local file
const uploadLocal = "";

// set to hosted URL to upload hosted file
const uploadHosted = "";

if (groundxKey === "YOUR_GROUNDX_KEY") {
  throw Error("set your GroundX key");
}


// initialize client
const groundx = new Groundx({
  apiKey: groundxKey,
});


if (bucketId === 0) {
  // list buckets
  const bucketResponse = await groundx.buckets.list();
  if (!bucketResponse || !bucketResponse.status || bucketResponse.status != 200 ||
      !bucketResponse.data || !bucketResponse.data.buckets) {
    console.error(bucketResponse);
    throw Error("GroundX bucket request failed");
  }

  if (bucketResponse.data.buckets.count < 1) {
    console.error("no results from buckets");
    console.log(bucketResponse.data.buckets);
    throw Error("no results from GroundX bucket query");
  }

  bucketId = bucketResponse.data.buckets[0].bucketId;
}


if (uploadLocal !== "" && fileType !== "" && fileName !== "") {
  // upload local documents to GroundX
  let ingest = await groundx.documents.uploadLocal([
    {
      blob: fs.readFileSync(uploadLocal),
      metadata: {
        bucketId: bucketId,
        fileName: fileName,
        fileType: fileType,
      },
    }
  ]);

  if (!ingest || !ingest.status || ingest.status != 200 ||
    !ingest.data || !ingest.data.ingest) {
    console.error(ingest);
    throw Error("GroundX upload request failed");
  }

  // poll ingest status
  while (ingest.data.ingest.status !== "complete" && ingest.data.ingest.status !== "error") {
    ingest = await groundx.documents.getProcessingStatusById({
      processId: ingest.data.ingest.processId,
    });
    if (!ingest || !ingest.status || ingest.status != 200 ||
      !ingest.data || !ingest.data.ingest) {
      console.error(ingest);
      throw Error("GroundX upload request failed");
    }

    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}

if (uploadHosted !== "" && fileType !== "") {
  // upload hosted documents to GroundX
  let ingest = await groundx.documents.uploadRemote({
    documents: [
      {
        bucketId: bucketId,
        fileType: fileType,
        sourceUrl: uploadHosted,
      }
    ]
  });

  if (!ingest || !ingest.status || ingest.status != 200 ||
    !ingest.data || !ingest.data.ingest) {
    console.error(ingest);
    throw Error("GroundX upload request failed");
  }

  // poll ingest status
  while (ingest.data.ingest.status !== "complete" && ingest.data.ingest.status !== "error") {
    ingest = await groundx.documents.getProcessingStatusById({
      processId: ingest.data.ingest.processId,
    });
    if (!ingest || !ingest.status || ingest.status != 200 ||
      !ingest.data || !ingest.data.ingest) {
      console.error(ingest);
      throw Error("GroundX upload request failed");
    }

    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}


if (projectId === 0) {
  // list projects
  const projResponse = await groundx.projects.list();
  if (!projResponse || !projResponse.status || projResponse.status != 200 ||
    !projResponse.data || !projResponse.data.projects) {
  console.error(projResponse);
  throw Error("GroundX project request failed");
  }

  if (projResponse.data.projects.count < 1) {
  console.error("no results from projects");
  console.log(projResponse.data.projects);
  throw Error("no results from GroundX project query");
  }

  projectId = projResponse.data.projects[0].projectId;
}

if (query !== "") {
  // search
  const searchResponse = await groundx.search.content({
    id: projectId,
    search: {
      query: query
    },
  });

  if (!searchResponse || !searchResponse.status || searchResponse.status != 200 ||
    !searchResponse.data || !searchResponse.data.search) {
    console.error(searchResponse);
    throw Error("GroundX search request failed");
  }

  if (searchResponse.data.search.count < 1) {
    console.error("no results from search");
    console.log(projResponse.data.search);
    throw Error("no results from GroundX search query");
  }

  console.log(searchResponse.data.search);
}
