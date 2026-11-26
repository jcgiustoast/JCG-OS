// Shape of edl.json, written by content/scripts/video/prep/edl.py.
// Times are seconds; media paths are relative to the Remotion public/ dir.

export type Box = { x: number; y: number; w: number; h: number };

export type Span = { srcStart: number; srcEnd: number; outStart: number };

export type Item = {
  score: number;
  shot: string;
  layout: "tall" | "wide";
  box: Box;
  crop: boolean;
  imgW: number;
  imgH: number;
  outStart: number;
  outEnd: number;
  redact: Box[]; // image pixels
};

export type Caption = { text: string; outStart: number; outEnd: number };

export type Edl = {
  format: "ranking";
  fps: number;
  width: number;
  height: number;
  video: string;
  duration: number;
  spans: Span[];
  items: Item[];
  captions: Caption[];
};

// Remotion props must be a plain record type.
export type EdlProps = Edl & Record<string, unknown>;

export const toFrame = (seconds: number, fps: number): number => Math.round(seconds * fps);

// Screenshot shows this long after its item's cut (the badge shows on the cut).
export const SHOT_DELAY = 0.2;
