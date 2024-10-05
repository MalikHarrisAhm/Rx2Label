import MainSheet from "@/components/sheet";
import { StyleSheet, Platform, SafeAreaView, StatusBar } from "react-native";

export default function HomeScreen() {
  return (
    <SafeAreaView style={styles.wrapper}>
      <MainSheet />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    paddingTop: ["android"].includes(Platform.OS) ? StatusBar.currentHeight : 0,
    backgroundColor: "#222",
    height: "100%",
    display: "flex",
  },
});
