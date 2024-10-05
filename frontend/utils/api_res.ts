import { SERVER_ROOT } from "./data";

export interface ImageProcessRes {
  prescriptionText: string;
  error: boolean;
  reason: string;
  validate_result: boolean;
}

export async function sendImageProcessRequest(
  imageBase64: string
): Promise<ImageProcessRes> {
  console.log("sending");
  const res = await fetch(SERVER_ROOT + "/process-image", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ base64_img: imageBase64 }),
  });
  return (await res.json()) as ImageProcessRes;
  //   return new Promise((res) =>
  //     res({
  //       prescriptionText: "test1",
  //       error: true,
  //       reason: "test3",
  //       validate_result: true,
  //     })
  //   );
}
