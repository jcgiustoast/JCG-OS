// Spoken words as plain white text: no box, soft shadow, centred under the
// badge column. One Sequence per phrase.
import React from "react";
import { Sequence } from "remotion";
import { Caption, toFrame } from "../edl";
import { CAPTION_FONT } from "../fonts";

export const Captions: React.FC<{
  captions: Caption[];
  fps: number;
  width: number;
  height: number;
}> = ({ captions, fps, width, height }) => {
  const blockW = Math.round(0.45 * width);
  const bandTop = Math.round(0.82 * height);
  const bandH = Math.round(0.88 * height) - bandTop;
  return (
    <>
      {captions.map((c, i) => {
        const from = toFrame(c.outStart, fps);
        const until = toFrame(c.outEnd, fps);
        if (until <= from) return null;
        return (
          <Sequence key={i} from={from} durationInFrames={until - from} layout="none">
            <div
              style={{
                position: "absolute",
                left: Math.round(0.65 * width - blockW / 2),
                top: bandTop,
                width: blockW,
                height: bandH,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <div
                style={{
                  fontFamily: CAPTION_FONT,
                  fontWeight: 500,
                  fontSize: 41,
                  lineHeight: 1.18,
                  color: "#fff",
                  textAlign: "center",
                  textWrap: "balance", // no lone last word ("... out of / 10")
                  textShadow: "0 2px 6px rgba(0,0,0,0.55), 0 0 2px rgba(0,0,0,0.35)",
                }}
              >
                {c.text}
              </div>
            </div>
          </Sequence>
        );
      })}
    </>
  );
};
