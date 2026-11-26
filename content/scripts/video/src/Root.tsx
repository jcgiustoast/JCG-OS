import React from "react";
import { CalculateMetadataFunction, Composition } from "remotion";
import sample from "../sample/edl.sample.json";
import { EdlProps } from "./edl";
import { Ranking } from "./Ranking";

const calculateMetadata: CalculateMetadataFunction<EdlProps> = ({ props }) => ({
  durationInFrames: Math.max(1, Math.ceil(props.duration * props.fps)),
  fps: props.fps,
  width: props.width,
  height: props.height,
});

export const Root: React.FC = () => (
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
);
