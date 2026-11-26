// The ranking short: face video, then per item its screenshot (0.2 s after
// the cut) and score badge (on the cut), then captions on top.
import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import { EdlProps, SHOT_DELAY, toFrame } from "./edl";
import "./fonts";
import { Badge } from "./parts/Badge";
import { Captions } from "./parts/Captions";
import { FaceTrack } from "./parts/FaceTrack";
import { Shot } from "./parts/Shot";

export const Ranking: React.FC<EdlProps> = (edl) => {
  const { fps, width, height } = edl;
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <FaceTrack video={edl.video} spans={edl.spans} fps={fps} />
      {edl.items.map((item, i) => {
        const end = toFrame(item.outEnd, fps);
        const shotFrom = toFrame(item.outStart + SHOT_DELAY, fps);
        const badgeFrom = toFrame(item.outStart, fps);
        return (
          <React.Fragment key={i}>
            {end > shotFrom && (
              <Sequence from={shotFrom} durationInFrames={end - shotFrom} layout="none">
                <Shot item={item} />
              </Sequence>
            )}
            {end > badgeFrom && (
              <Sequence from={badgeFrom} durationInFrames={end - badgeFrom} layout="none">
                <Badge score={item.score} width={width} height={height} />
              </Sequence>
            )}
          </React.Fragment>
        );
      })}
      <Captions captions={edl.captions} fps={fps} width={width} height={height} />
    </AbsoluteFill>
  );
};
