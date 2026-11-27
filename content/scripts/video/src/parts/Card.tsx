// A picture as a rounded card with a soft shadow, in the top half of the frame.
// The box is already contain-fitted by prep, so the image fills it exactly.
import React from "react";
import { Img, staticFile } from "remotion";
import { Picture } from "../edl";
import { LAYOUT } from "../layout";
import { Redactions } from "./Shot";

export const Card: React.FC<{ picture: Picture }> = ({ picture }) => {
  const { box, imgW, redact } = picture;
  return (
    <div
      style={{
        position: "absolute",
        left: box.x,
        top: box.y,
        width: box.w,
        height: box.h,
        borderRadius: LAYOUT.transparent.card.radius,
        boxShadow: "0 8px 28px rgba(0,0,0,0.35)",
        overflow: "hidden",
      }}
    >
      <Img
        src={staticFile(picture.shot)}
        style={{ position: "absolute", left: 0, top: 0, width: box.w, height: box.h, display: "block" }}
      />
      <Redactions redact={redact} scale={box.w / imgW} />
    </div>
  );
};
