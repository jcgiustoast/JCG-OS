import React from "react";
import { Composition } from "remotion";
import sample from "../sample/edl.sample.json";
import transparentSample from "../sample/edl.transparent.sample.json";
import { EdlProps, TransparentProps } from "./edl";
import { Ranking } from "./Ranking";
import { TransparentBackground } from "./TransparentBackground";

const calculateMetadata = ({ props }: { props: { duration: number; fps: number; width: number; height: number } }) => ({
  durationInFrames: Math.max(1, Math.ceil(props.duration * props.fps)),
  fps: props.fps,
  width: props.width,
  height: props.height,
});

export const Root: React.FC = () => (
  <>
  <Composition
    id="Ranking"
    component={Ranking}
    defaultProps={sample as EdlProps}
    calculateMetadata={calculateMetadata}
    durationInFrames={1}
    fps={30}
    width={1080}
    height={1920}
  />
  <Composition
    id="TransparentBackground"
    component={TransparentBackground}
    defaultProps={transparentSample as unknown as TransparentProps}
    calculateMetadata={calculateMetadata}
    durationInFrames={1}
    fps={30}
    width={1080}
    height={1920}
  />
  </>
);
