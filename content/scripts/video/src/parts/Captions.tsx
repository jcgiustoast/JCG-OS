// Spoken words as plain white text: no box, soft shadow. The box comes from
// edl.json (prep/edl.py): right of the screenshot column, at the bottom of the
// safe area, so no app overlay and no screenshot ever covers it. Text sits on
// the box's bottom edge, so one- and two-line phrases share a baseline.
import React from "react";
import { Sequence } from "remotion";
import { Box, Caption, toFrame } from "../edl";
import { CAPTION_FONT } from "../fonts";
import { LAYOUT } from "../layout";

// strongShadow (off by default, so the ranking look is unchanged): layered dark
// shadows, tight plus wide and soft, so white text still reads over a white page.
// No box, no outline.
const STRONG_SHADOW =
  "0 0 2px rgba(0,0,0,0.95), 0 0 6px rgba(0,0,0,0.85), 0 2px 12px rgba(0,0,0,0.7)";
const DEFAULT_SHADOW = "0 2px 6px rgba(0,0,0,0.55), 0 0 2px rgba(0,0,0,0.35)";

export const Captions: React.FC<{
  captions: Caption[];
  box: Box;
  fps: number;
  strongShadow?: boolean;
}> = ({
  captions,
  box,
  fps,
  strongShadow = false,
}) => (
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
              left: box.x,
              top: box.y,
              width: box.w,
              height: box.h,
              display: "flex",
              alignItems: "flex-end",
              justifyContent: "center",
            }}
          >
            <div
              style={{
                fontFamily: CAPTION_FONT,
                fontWeight: 500,
                fontSize: LAYOUT.caption.fontSize,
                lineHeight: LAYOUT.caption.lineHeight,
                color: "#fff",
                textAlign: "center",
                textWrap: "balance", // no lone last word ("... out of / 10")
                textShadow: strongShadow ? STRONG_SHADOW : DEFAULT_SHADOW,
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
