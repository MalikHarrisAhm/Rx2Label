"use client";

import { useState } from "react";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async (event) => {
    event.preventDefault();
    if (!selectedFile) {
      alert("Please select a file first!");
      return;
    }

    setIsLoading(true);

    try {
      // Convert the file to base64
      const base64String = await convertToBase64(selectedFile);
      console.log(base64String);

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

  const convertToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result.split(",")[1]);
      reader.onerror = (error) => reject(error);
    });
  };

  return (
    <div className="">
      <form>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button onClick={handleUpload}>Send</button>
        {response}
      </form>
    </div>
  );
}
