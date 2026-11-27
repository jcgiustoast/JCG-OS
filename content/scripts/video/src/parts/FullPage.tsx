// A picture filling the frame: scaled to the frame width, top-anchored. A very
// tall page shows its top part. Juan's cut-out is drawn over it by the caller.
import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { Picture } from "../edl";
import { Redactions } from "./Shot";

export const FullPage: React.FC<{ picture: Picture }> = ({ picture }) => {
  const { box, imgW, imgH, redact } = picture;
  const scale = box.w / imgW;
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#000" }}>
      <Img
        src={staticFile(picture.shot)}
        style={{ position: "absolute", left: 0, top: 0, width: box.w, height: imgH * scale, display: "block" }}
      />
      <Redactions redact={redact} scale={scale} />
    </AbsoluteFill>
  );
};
