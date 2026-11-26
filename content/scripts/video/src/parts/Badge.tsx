// The score badge: black rounded box, white score, purple "/10".
// Position and minimum size are fixed fractions of the frame; a two-digit
// score ("10/10") lets the box grow to the right instead of shrinking the text.
import React from "react";
import { BADGE_FONT } from "../fonts";

const PURPLE = "#B084D3";

export const Badge: React.FC<{ score: number; width: number; height: number }> = ({
  score,
  width,
  height,
}) => {
  const boxH = Math.round(0.055 * height);
  return (
    <div
      style={{
        position: "absolute",
        left: Math.round(0.68 * width),
        top: Math.round(0.26 * height),
        minWidth: Math.round(0.16 * width),
        height: boxH,
        padding: "0 18px",
        boxSizing: "border-box",
        background: "#000",
        borderRadius: 14,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: BADGE_FONT,
        fontWeight: 500,
        fontSize: Math.round(boxH * 0.62),
        lineHeight: 1,
        whiteSpace: "nowrap",
      }}
    >
      <span style={{ color: "#fff" }}>{score}</span>
      <span style={{ color: PURPLE }}>/10</span>
    </div>
  );
};
