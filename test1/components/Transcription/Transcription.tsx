import { Data } from "@/app/page";
import { Skeleton } from "../ui/skeleton";
import { useEffect } from "react";

export default function Transcription({
  data,
  setData,
  setLoading,
}: {
  data: Data;
  setData: (data: Data | ((data: Data) => Data)) => void;
  setLoading: (data: boolean | ((data: boolean) => boolean)) => void;
}) {
  useEffect(() => {
    const fetchNextData = async () => {
      if (data.tanscription) {
        console.log("fetching data");
        try {
          setLoading(true);
          const response = await fetch("http://localhost:8000/process-rx", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              text: data.tanscription,
            }),
          });

          const result = await response.json();
          setData((prev) => ({ ...prev, ...result }));
        } catch (error) {
          console.error("Error fetching next data:", error);
          setData({ tanscription: undefined });
        } finally {
          setLoading(false);
        }
      }
    };

    fetchNextData();
  }, [data.tanscription]);

  return (
    <div className="flex max-w-[25vw] flex-col gap-3">
      <h1>Transcription</h1>
      {data.tanscription ? (
        <p>{data.tanscription}</p>
      ) : (
        [1, 2, 3].map((_, i) => <Skeleton key={i} className="h-4 w-[250px]" />)
      )}
    </div>
  );
}
