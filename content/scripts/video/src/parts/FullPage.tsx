// A picture covering the frame: scaled to the frame width (or more, if the page
// is shorter than the frame, so no black shows), top-anchored and centred
// sideways. A very tall page shows its top part. Juan's cut-out is drawn over it by the caller.
import React from "react";
import { AbsoluteFill, Img, staticFile, useVideoConfig } from "remotion";
import { Picture } from "../edl";
import { Redactions } from "./Shot";

export const FullPage: React.FC<{ picture: Picture }> = ({ picture }) => {
  const { imgW, imgH, redact } = picture;
  const { width, height } = useVideoConfig();
  const scale = Math.max(width / imgW, height / imgH);
  const left = (width - imgW * scale) / 2;
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#000" }}>
      <Img
        src={staticFile(picture.shot)}
        style={{ position: "absolute", left, top: 0, width: imgW * scale, height: imgH * scale, display: "block" }}
      />
      <div style={{ position: "absolute", left, top: 0 }}>
        <Redactions redact={redact} scale={scale} />
      </div>
    </AbsoluteFill>
  );
};
