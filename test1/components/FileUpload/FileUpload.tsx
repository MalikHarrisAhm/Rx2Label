"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "../ui/input";
import Image from "next/image";

export default function FileUpload() {
  const [base64String, setBase64String] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState(null);

  const handleFileChange = async (event) => {
    const tmp: string = await convertToBase64(event.target.files[0]);
    console.log(tmp);
    setBase64String(tmp);
  };

  const handleUpload = async (event) => {
    event.preventDefault();
    if (!base64String) {
      alert("Please select a file first!");
      return;
    }

    setIsLoading(true);
    try {
      // Send the base64 string to the backend
      const response = await fetch("http://localhost:8000/process-image", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ base64_img: base64String }),
      });

      const data = await response.json();
      setResponse(data);
    } catch (error) {
      console.error("Error uploading image:", error);
      setResponse({ error: "Failed to upload image" });
    } finally {
      setIsLoading(false);
    }
  };

  const convertToBase64 = (file): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result.split(",")[1]);
      reader.onerror = (error) => reject(error);
    });
  };

  return (
    <div className="flex flex-col justify-center items-center gap-3 h-full p-10">
      {base64String && (
        <img
          src={`data:image/jpeg;base64,${base64String}`}
          alt="Base64 Image"
          style={{ width: "100%", height: "auto", maxWidth: "300px" }}
        />
      )}
      <Input type="file" accept="image/*" onChange={handleFileChange} />
      <Button onClick={handleUpload} disabled={isLoading}>
        Process
      </Button>
    </div>
  );
}
