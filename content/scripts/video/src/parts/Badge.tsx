// The score badge: black rounded box, white score, purple "/10".
// Anchored to its screenshot's top-right corner (prep/edl.py works out where),
// so it follows the screenshot and stays off the face. A two-digit score
// ("10/10") makes the box grow to the left instead of shrinking the text.
import React from "react";
import { BadgeAnchor } from "../edl";
import { BADGE_FONT } from "../fonts";
import { LAYOUT } from "../layout";

export const Badge: React.FC<{ score: number; anchor: BadgeAnchor; width: number }> = ({
  score,
  anchor,
  width,
}) => {
  const { minWidth, radius, padX, fontScale, purple } = LAYOUT.badge;
  return (
    <div
      style={{
        position: "absolute",
        right: width - anchor.right,
        top: anchor.top,
        minWidth,
        height: anchor.h,
        padding: `0 ${padX}px`,
        boxSizing: "border-box",
        background: "#000",
        borderRadius: radius,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: BADGE_FONT,
        fontWeight: 500,
        fontSize: Math.round(anchor.h * fontScale),
        lineHeight: 1,
        whiteSpace: "nowrap",
      }}
    >
      <span style={{ color: "#fff" }}>{score}</span>
      <span style={{ color: purple }}>/10</span>
    </div>
  );
};
