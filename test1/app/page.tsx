"use client";

import FileUpload from "../components/FileUpload/FileUpload";
import { useState } from "react";
import Transcription from "../components/Transcription/Transcription";
import Checks from "@/components/Checks/Checks";

export interface Data {
  tanscription?: string;
  error?: boolean;
  reason?: string;
  smpc_quote?: string;
  smpc_quote_valid?: boolean;
}

export default function Home() {
  const [data, setData] = useState<Data>({});
  const [transcriptLoading, setTranscriptLoading] = useState(false);
  const [smpcLoading, setSmpcLoading] = useState(false);

  return (
    <div className="flex flex-row gap-10 justify-center items-center h-full w-full">
      <FileUpload
        setLoading={setTranscriptLoading}
        loading={transcriptLoading}
        setData={setData}
      />
      {(transcriptLoading || data.tanscription) && (
        <Transcription
          data={data}
          setData={setData}
          setLoading={setSmpcLoading}
        />
      )}
      {(smpcLoading || data.error !== undefined) && <Checks data={data} />}
    </div>
  );
}
