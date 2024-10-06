"use client";

import FileUpload from "../components/FileUpload/FileUpload";
import { useState } from "react";

interface Data {
  tanscription: string;
  error: boolean;
  reason: string;
  smpc_quote: string;
  smpc_quote_valid: boolean;
}

export default function Home() {
  const [data, setData] = useState({});

  return (
    <div className="flex justify-center items-center h-full w-full">
      <FileUpload />
    </div>
  );
}
