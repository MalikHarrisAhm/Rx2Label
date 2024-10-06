import { Data } from "@/app/page";
import {
  CheckCircleIcon,
  ExclamationTriangleIcon,
} from "@heroicons/react/24/outline";
import { Skeleton } from "../ui/skeleton";
import React, { useEffect } from "react";

export default function Checks({ data }: { data: Data }) {
  const [label, setLabel] = React.useState<{
    drug_name: string;
    directions: string;
  } | null>(null);

  useEffect(() => {
    const init = async () => {
      if (data.error === false) {
        try {
          const res = await fetch("http://localhost:8000/get-label", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              text: data.tanscription,
            }),
          });
          const label = ((await res.json()) as string)
            .replaceAll("`", "")
            .replaceAll("json", "");
          console.log(label);
          const parsed = JSON.parse(label);
          console.log(parsed);
          setLabel(parsed);
        } catch (error) {
          console.error("Error fetching next data:", error);
          setLabel(null);
        }
      } else {
        setLabel(null);
      }
    };

    init();
  }, [data.error]);

  return (
    <div className="flex flex-col gap-5 max-w-[30vw]">
      {label == null && data.error === false && (
        <Skeleton className="w-[30vw] h-[176px]" />
      )}
      {label && (
        <div className="!w-30vw !h-300px bg-white flex rounded-md flex-row text-black p-5">
          <div className="flex flex-col">
            <p>{label?.drug_name}</p>
            <p className="pb-10">{label?.directions}</p>
            <p className="flex-1 font-bold text-green-600">PHARMACY</p>
          </div>
          <div className="flex-1 flex flex-col items-end justify-end">
            <p>06/10/2024</p>
          </div>
        </div>
      )}
      {data.error === undefined ? (
        <div className="flex flex-col justify-center items-center">
          {/* <p>
            Checking the latest SMPC for Paracetmol to determine the clinical
            accuracy of the prescription...
          </p> */}
          <div className="flex flex-row gap-2 items-center">
            <Skeleton className="h-12 w-12 rounded-full" />
            <Skeleton className="h-4 w-[300px]" />
          </div>
        </div>
      ) : (
        <div className="flex flex-col gap-5">
          <div className="flex flex-row gap-2 items-center">
            {data.error ? (
              <ExclamationTriangleIcon className="w-6 h-6 text-red-500" />
            ) : (
              <CheckCircleIcon className="w-6 h-6 text-green-500" />
            )}
            <p className="max-w-[25vw]">
              {data.error
                ? "Clinical Error Detected."
                : "Passed Clinical Check."}
            </p>
          </div>
          {data.reason !== undefined && <p>{data.reason}</p>}
        </div>
      )}
    </div>
  );
}
