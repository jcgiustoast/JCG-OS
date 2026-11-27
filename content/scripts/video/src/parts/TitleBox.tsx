// The headline box for the first seconds: black, white Big Shoulders, one line
// per div as prep/title.py fitted them. Placed from the edl; no animation.
import React from "react";
import { TitleLayout } from "../edl";
import { TITLE_FONT } from "../fonts";

export const TitleBox: React.FC<{ title: TitleLayout }> = ({ title }) => {
  const { box, lines, fontSize, lineHeight } = title;
  return (
    <div
      style={{
        position: "absolute",
        left: box.x,
        top: box.y,
        width: box.w,
        height: box.h,
        background: "#000",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        fontFamily: TITLE_FONT,
        fontWeight: 800,
        fontSize,
        lineHeight,
        color: "#fff",
        textAlign: "center",
      }}
    >
      {lines.map((line, i) => (
        <div key={i} style={{ whiteSpace: "nowrap" }}>
          {line}
        </div>
      ))}
    </div>
  );
};
