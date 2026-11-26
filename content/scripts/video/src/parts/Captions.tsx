// Spoken words as plain white text: no box, soft shadow, centred on x 65%
// in the 82-88% band. One Sequence per phrase.
import React from "react";
import { Sequence } from "remotion";
import { Caption, Item, toFrame } from "../edl";
import { CAPTION_FONT } from "../fonts";

const GAP_TO_SHOT = 16; // px kept clear between caption text and a screenshot

// Block width: 45% of the frame, narrowed when the screenshot on screen
// reaches down into the caption band (very tall shots), so white text never
// runs onto a light screenshot.
const blockWidth = (
  item: Item | undefined,
  width: number,
  centre: number,
  bandTop: number,
  bandBottom: number,
): number => {
  const max = Math.round(0.45 * width);
  if (!item) return max;
  const { x, y, w, h } = item.box;
  const overlapsBand = y < bandBottom && y + h > bandTop;
  if (!overlapsBand) return max;
  const room = 2 * (centre - (x + w) - GAP_TO_SHOT);
  return Math.max(200, Math.min(max, room));
};

export const Captions: React.FC<{
  captions: Caption[];
  items: Item[];
  fps: number;
  width: number;
  height: number;
}> = ({ captions, items, fps, width, height }) => {
  const centre = Math.round(0.65 * width);
  const bandTop = Math.round(0.82 * height);
  const bandBottom = Math.round(0.88 * height);
  return (
    <>
      {captions.map((c, i) => {
        const from = toFrame(c.outStart, fps);
        const until = toFrame(c.outEnd, fps);
        if (until <= from) return null;
        const item = items.find((it) => it.outStart <= c.outStart + 1e-6 && c.outStart < it.outEnd);
        const blockW = blockWidth(item, width, centre, bandTop, bandBottom);
        return (
          <Sequence key={i} from={from} durationInFrames={until - from} layout="none">
            <div
              style={{
                position: "absolute",
                left: Math.round(centre - blockW / 2),
                top: bandTop,
                width: blockW,
                height: bandBottom - bandTop,
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
