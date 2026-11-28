// The Transparent Background short: Juan's face video (with the voice), then
// per picture either a card (top half) or a full-screen page with Juan cut out
// in front of it, then the headline box for the first seconds, captions on top.
import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import { TransparentProps, toFrame } from "./edl";
import "./fonts";
import { Captions } from "./parts/Captions";
import { Card } from "./parts/Card";
import { FaceTrack } from "./parts/FaceTrack";
import { FullPage } from "./parts/FullPage";
import { TitleBox } from "./parts/TitleBox";
import { LAYOUT } from "./layout";

// the cut-out is drawn smaller, tucked into the bottom-left, body running off the edges
const CUT = LAYOUT.transparent.cutout;
const CUT_STYLE: React.CSSProperties = {
  position: "absolute",
  left: CUT.x,
  top: CUT.bottom - 1920 * CUT.scale,
  width: 1080,
  height: 1920,
  transform: `scale(${CUT.scale})`,
  transformOrigin: "top left",
};

export const TransparentBackground: React.FC<TransparentProps> = (edl) => {
  const { fps } = edl;
  const titleEnd = toFrame(edl.title.outEnd, fps);
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <FaceTrack video={edl.video} spans={edl.spans} fps={fps} />
      {edl.pictures.map((p, i) => {
        const from = toFrame(p.outStart, fps);
        const end = toFrame(p.outEnd, fps);
        if (p.show !== "full" || end <= from) return null;
        return (
          <React.Fragment key={i}>
            <Sequence from={from} durationInFrames={end - from} layout="none">
              <FullPage picture={p} />
            </Sequence>
            {p.matte && (
              // matte spans carry absolute outStarts, so this sits outside the Sequence
              <div style={CUT_STYLE}>
                <FaceTrack video={p.matte.file} spans={p.matte.spans} fps={fps} muted />
              </div>
            )}
          </React.Fragment>
        );
      })}
      {edl.pictures.map((p, i) => {
        const from = toFrame(p.outStart, fps);
        const end = toFrame(p.outEnd, fps);
        if (p.show !== "card" || end <= from) return null;
        return (
          <Sequence key={i} from={from} durationInFrames={end - from} layout="none">
            <Card picture={p} />
          </Sequence>
        );
      })}
      {titleEnd > 0 && (
        <Sequence from={0} durationInFrames={titleEnd} layout="none">
          <TitleBox title={edl.title} />
        </Sequence>
      )}
      <Captions captions={edl.captions} box={edl.caption} fps={fps} strongShadow />
    </AbsoluteFill>
  );
};
