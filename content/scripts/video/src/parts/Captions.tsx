// Spoken words as plain white text: no box, soft shadow. The box comes from
// edl.json (prep/edl.py): right of the screenshot column, at the bottom of the
// safe area, so no app overlay and no screenshot ever covers it. Text sits on
// the box's bottom edge, so one- and two-line phrases share a baseline.
import React from "react";
import { Sequence } from "remotion";
import { Box, Caption, toFrame } from "../edl";
import { CAPTION_FONT } from "../fonts";
import { LAYOUT } from "../layout";

// boxed (off by default, so the ranking look is unchanged): each phrase sits in
// a solid black box that hugs its lines, like the Transparent Background title
// box, so white text reads over any picture.
export const Captions: React.FC<{
  captions: Caption[];
  box: Box;
  fps: number;
  boxed?: boolean;
}> = ({
  captions,
  box,
  fps,
  boxed = false,
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
                textShadow: boxed
                  ? "none"
                  : "0 2px 6px rgba(0,0,0,0.55), 0 0 2px rgba(0,0,0,0.35)",
              }}
            >
              {boxed ? (
                <span
                  style={{
                    background: "#000",
                    padding: "10px 18px",
                    WebkitBoxDecorationBreak: "clone",
                    boxDecorationBreak: "clone",
                    // padding sits on the first/last line only horizontally; lines stack tight
                    lineHeight: 1.45,
                  }}
                >
                  {c.text}
                </span>
              ) : (
                c.text
              )}
            </div>
          </div>
        </Sequence>
      );
    })}
  </>
);
