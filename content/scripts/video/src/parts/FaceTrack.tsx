// The face recording with pauses removed: one Sequence per kept span, each
// playing its own slice of the source file, laid end to end.
import React from "react";
import { AbsoluteFill, OffthreadVideo, Sequence, staticFile } from "remotion";
import { Span, toFrame } from "../edl";

export const FaceTrack: React.FC<{ video: string; spans: Span[]; fps: number }> = ({
  video,
  spans,
  fps,
}) => {
  const src = staticFile(video);
  return (
    <AbsoluteFill>
      {spans.map((span, i) => {
        const from = toFrame(span.outStart, fps);
        const next = spans[i + 1];
        const until = next
          ? toFrame(next.outStart, fps)
          : toFrame(span.outStart + (span.srcEnd - span.srcStart), fps);
        return (
          <Sequence key={i} from={from} durationInFrames={Math.max(1, until - from)} layout="none">
            <AbsoluteFill>
              <OffthreadVideo
                src={src}
                trimBefore={toFrame(span.srcStart, fps)}
                style={{ width: "100%", height: "100%", objectFit: "cover" }}
              />
            </AbsoluteFill>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
