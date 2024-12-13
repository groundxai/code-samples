import { GroundXClient } from "groundx";

import dotenv from 'dotenv'; 
dotenv.config();

if (!process.env.GROUNDX_API_KEY) {
  throw new Error("You have not set a required environment variable (GROUNDX_API_KEY or OPENAI_API_KEY). Copy .env.sample and rename it to .env then fill in the missing values.");
}

const opts = {
  bucketId: null,
  fileType: "pdf",
  fileName: "attention.pdf",
  pathOrUrl: "/home/celestial/Documents/projects/eyelevel/code-samples/typescript/getting-started/attention.pdf",
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

const ingest = async bucketId => {
  // upload local documents to GroundX
  let ingest = await client.ingest([
    {
      bucketId: bucketId,
      filePath: opts.pathOrUrl,
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


let bucketId = opts.bucketId;
if (!bucketId) bucketId = await usingBucket();

if (!opts.pathOrUrl || !opts.fileType || !opts.fileName) {
  throw new Error("pathOrUrl/fileType/fileName is not set");
}

await ingest(bucketId);

