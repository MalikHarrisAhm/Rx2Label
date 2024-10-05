import React, { useRef, useState } from "react";
import { Sheet, Button, Spinner } from "tamagui";
import { Image, StyleSheet, View, Text } from "react-native";
import { useCameraPermissions, CameraView } from "expo-camera";
import { ImageProcessRes, sendImageProcessRequest } from "@/utils/api_res";

const SNAP_POINTS = [90, 15];

export default function MainSheet() {
  const [takePhoto, setTakePhoto] = useState(false);
  const [permission, askPermission] = useCameraPermissions();
  const cameraRef = useRef<CameraView>(null);
  const [image, setImage] = useState<string | undefined>(undefined);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ImageProcessRes | undefined>(undefined);

  async function takePicture() {
    if (cameraRef.current) {
      const photo = await cameraRef.current.takePictureAsync({ base64: true });
      setImage(
        photo?.base64 !== undefined
          ? `data:image/jpeg;base64,${photo.base64}`
          : undefined
      );
    }
  }

  async function processImage() {
    // send image to the backend to process with mistral
    setLoading(true);
    if (image) {
      const res = await sendImageProcessRequest(image);
      console.log(res);
      setResult(res);
      setLoading(false);
    }
  }

  return (
    <Sheet modal={true} open={true} snapPoints={SNAP_POINTS}>
      <View style={styles.sheet}>
        <Button
          onPress={() => {
            if (permission && !permission.granted) {
              askPermission();
            } else if (permission) {
              setTakePhoto((prev) => !prev);
              setLoading(false);
              setResult(undefined);
              setImage(undefined);
            }
          }}
        >
          {takePhoto ? "Stop" : "Take a photo of the prescription"}
        </Button>
        {takePhoto && image === undefined && (
          <CameraView ref={cameraRef} style={styles.camera} facing={"back"}>
            <View style={styles.buttonContainer}>
              <Button onPress={takePicture}>Take Photo</Button>
            </View>
          </CameraView>
        )}
        {takePhoto &&
          image !== undefined &&
          (loading ? (
            <View
              style={{
                flex: 1,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <Spinner size="large" />
            </View>
          ) : (
            <View style={styles.imageContainer}>
              <Image
                source={{
                  uri: image,
                }}
                style={{ width: 200, height: 400, borderRadius: 10 }}
              />
              {result !== undefined ? (
                <>
                  <View style={styles.resultBox}>
                    <Text style={styles.resultTitle}>
                      Prescription Text Read
                    </Text>
                    <Text style={styles.resultText}>
                      {result.prescriptionText}
                    </Text>
                  </View>

                  <View style={styles.resultBox}>
                    <Text
                      style={{
                        ...styles.resultTitle,
                        backgroundColor: result.error ? "#FF6961" : "#49cc90",
                        borderRadius: 10,
                        padding: 8,
                        textAlign: "center",
                      }}
                    >
                      Error
                    </Text>
                    <Text style={styles.resultText}>{result.reason}</Text>
                  </View>
                </>
              ) : (
                <>
                  <Text style={styles.imageText}>Select this image?</Text>
                  <View style={styles.imageButtonContainer}>
                    <Button
                      onPress={() => setImage(undefined)}
                      style={styles.imageButton}
                    >
                      No
                    </Button>
                    <Button onPress={processImage} style={styles.imageButton}>
                      Yes
                    </Button>
                  </View>
                </>
              )}
            </View>
          ))}
      </View>
    </Sheet>
  );
}

const RADIUS = 30;
const styles = StyleSheet.create({
  sheet: {
    padding: 40,
    backgroundColor: "#111",
    borderTopLeftRadius: RADIUS,
    borderTopRightRadius: RADIUS,
    height: "100%",
    display: "flex",
    color: "#fff",
    gap: 20,
  },
  camera: {
    flex: 1,
    borderRadius: RADIUS,
  },
  buttonContainer: {
    flex: 1,
    flexDirection: "column",
    backgroundColor: "transparent",
    justifyContent: "flex-end",
    padding: 20,
  },
  imageContainer: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 20,
  },
  imageText: {
    color: "#fff",
    fontSize: 20,
  },
  imageButtonContainer: {
    width: "100%",
    display: "flex",
    flexDirection: "row",
    gap: 10,
    paddingLeft: 20,
    paddingRight: 20,
  },
  imageButton: {
    flex: 1,
  },
  resultBox: {
    width: "100%",
    display: "flex",
    flexDirection: "column",
    backgroundColor: "#333",
    borderRadius: 15,
    padding: 15,
    gap: 5,
  },
  resultTitle: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#fff",
  },
  resultText: {
    color: "#fff",
    fontSize: 16,
  },
});
