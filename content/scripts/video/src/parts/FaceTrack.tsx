// The face recording with pauses removed: one Sequence per kept span, each
// playing its own slice of the source file, laid end to end.
//
// Small joins are softened over a couple of frames: the span before keeps
// playing (muted) underneath for `blendFrames` extra frames while the next one
// fades in on top. A cut that removes only a fraction of a second shifts the
// head a little; as a hard switch that reads as a dropped-frame stutter,
// blended it reads as a quick move. Joins that remove more than
// `blendMaxRemoved` seconds stay hard cuts: the head moved a lot, a blend would
// show a double face, and a clean jump cut reads as a deliberate edit.
import React from "react";
import { AbsoluteFill, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame } from "remotion";
import { Span, toFrame } from "../edl";
import { LAYOUT } from "../layout";

const BLEND = LAYOUT.cut.blendFrames;
const BLEND_MAX_REMOVED = LAYOUT.cut.blendMaxRemoved;

const blendInto = (a: Span | undefined, b: Span | undefined): number =>
  a && b && b.srcStart - a.srcEnd <= BLEND_MAX_REMOVED ? BLEND : 0;

const FadeIn: React.FC<{ frames: number; children: React.ReactNode }> = ({ frames, children }) => {
  const frame = useCurrentFrame();
  // first frame already part-way in, so the cut lands on its own frame
  const opacity = frames > 0 ? interpolate(frame, [-1, frames], [0, 1], { extrapolateRight: "clamp" }) : 1;
  return <AbsoluteFill style={{ opacity }}>{children}</AbsoluteFill>;
};

export const FaceTrack: React.FC<{
  video: string;
  spans: Span[];
  fps: number;
  transparent?: boolean; // the file has an alpha channel (cut-out clip)
  muted?: boolean;
}> = ({ video, spans, fps, transparent = false, muted = false }) => {
  const src = staticFile(video);
  return (
    <AbsoluteFill>
      {spans.map((span, i) => {
        const from = toFrame(span.outStart, fps);
        const next = spans[i + 1];
        const until = next
          ? toFrame(next.outStart, fps)
          : toFrame(span.outStart + (span.srcEnd - span.srcStart), fps);
        const own = Math.max(1, until - from);
        const tail = blendInto(span, next); // keep showing under the next span's fade-in
        return (
          <Sequence key={i} from={from} durationInFrames={own + tail} layout="none">
            <FadeIn frames={blendInto(spans[i - 1], span)}>
              <OffthreadVideo
                src={src}
                trimBefore={toFrame(span.srcStart, fps)}
                volume={(f) => (!muted && f < own ? 1 : 0)}
                transparent={transparent}
                style={{ width: "100%", height: "100%", objectFit: "cover" }}
              />
            </FadeIn>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
