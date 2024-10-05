import { Stack } from "expo-router";
import { StyleSheet } from "react-native";
import React from "react";

export default function NotFoundScreen() {
  return (
    <>
      <Stack.Screen options={{ title: "Oops!" }} />
    </>
  );
}
