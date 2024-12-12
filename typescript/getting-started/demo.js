import { GroundXClient } from "groundx";

import dotenv from 'dotenv'; 
dotenv.config();

if (!process.env.GROUNDX_API_KEY) {
  throw new Error("You have not set a required environment variable (GROUNDX_API_KEY or OPENAI_API_KEY). Copy .env.sample and rename it to .env then fill in the missing values.");
}

const opts = {
  query: "Transformer",
  bucketId: null,
  fileType: "pdf",
  fileName: "attention.pdf",
  localFilePath: "/home/celestial/Documents/projects/eyelevel/code-samples/typescript/getting-started/attention.pdf",
  remoteUrl: null
};

// initialize client
const client = new GroundXClient({
  apiKey: process.env.GROUNDX_API_KEY,
});

const usingBucket = async () => {
  // list buckets
  const buckets = await client.buckets.list().catch(err => {
    throw new Error("GroundX bucket request failed" + err);
  });

  if (buckets.buckets.count < 1) {
    throw new Error("no results from GroundX bucket query");
  }

  return buckets.buckets[0].bucketId;
}

const ingest = async (bucketId, filePath) => {
  // upload local documents to GroundX
  let ingest = await client.ingest([
    {
      bucketId: bucketId,
      filePath: filePath,
      fileName: opts.fileName,
      fileType: opts.fileType
    }
  ]).catch(err => {
    throw new Error("GroundX upload request failed: " + err);
  });

  // poll ingest status
  while (ingest.ingest.status !== "complete" &&
    ingest.ingest.status !== "error" &&
    ingest.ingest.status !== "cancelled") {
    ingest = await client.documents.getProcessingStatusById(ingest.ingest.processId).catch(err => {
      throw new Error("GroundX upload request failed: " + err);
    });

    await new Promise((resolve) => setTimeout(resolve, 3000));
  }

  return ingest
}


const search = async bucketId => {
  const searchResponse = await client.search.content(bucketId, {
    query: opts.query
  }).catch(err => {
    throw new Error("GroundX search request failed: " + err);
  });

  if (!searchResponse.search.text) {
    console.log(searchResponse.search);
    throw new Error("no results from GroundX search query");
  }

  console.log(searchResponse.search.text);
};

let bucketId = opts.bucketId;
if (!bucketId) bucketId = await usingBucket();

if (opts.localFilePath && !(opts.fileType && opts.fileName)) {
  throw new Error("local filepath is set but fileType/fileName is not");
}

if (opts.remoteUrl && !(opts.fileType && opts.fileName)) {
  throw new Error("remote url is set but fileType/fileName is not");
}

if (opts.localFilePath) await ingest(bucketId, opts.localFilePath);
if (opts.remoteUrl) await ingest(bucketId, opts.remoteUrl);
if (opts.query) await search(bucketId);

