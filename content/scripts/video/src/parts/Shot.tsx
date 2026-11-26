// One screenshot, placed flat on the video: no border, shadow, rounding or
// animation. Tall images that don't fit the column show their top part.
import React from "react";
import { Img, staticFile } from "remotion";
import { Item } from "../edl";

export const Shot: React.FC<{ item: Item }> = ({ item }) => {
  const { box, imgW, imgH, crop, redact } = item;
  const scale = box.w / imgW; // the image always fills the box width
  const imgHeight = crop ? imgH * scale : box.h;
  return (
    <div
      style={{
        position: "absolute",
        left: box.x,
        top: box.y,
        width: box.w,
        height: box.h,
        overflow: "hidden",
      }}
    >
      <Img
        src={staticFile(item.shot)}
        style={{ position: "absolute", left: 0, top: 0, width: box.w, height: imgHeight, display: "block" }}
      />
      {redact.map((r, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: r.x * scale,
            top: r.y * scale,
            width: r.w * scale,
            height: r.h * scale,
            background: "#000",
          }}
        />
      ))}
    </div>
  );
};
