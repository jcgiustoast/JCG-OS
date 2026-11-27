// Shape of edl.json, written by content/scripts/video/prep/edl.py.
// Times are seconds; media paths are relative to the Remotion public/ dir.

export type Box = { x: number; y: number; w: number; h: number };

export type Span = { srcStart: number; srcEnd: number; outStart: number };

// Score badge anchor (px): right edge and top; it grows leftwards for "10/10".
export type BadgeAnchor = { right: number; top: number; h: number };

export type Item = {
  score: number;
  shot: string;
  layout: "tall" | "wide";
  box: Box;
  badge: BadgeAnchor;
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
  safe: Box; // area Reels/TikTok overlays leave clear; everything drawn stays inside
  caption: Box; // where caption text sits (bottom-aligned), clear of every screenshot
  spans: Span[];
  items: Item[];
  captions: Caption[];
};

// Remotion props must be a plain record type.
export type EdlProps = Edl & Record<string, unknown>;

// ---- Transparent Background look (prep/transparent.py) ----

export type TitleLayout = {
  lines: string[];
  fontSize: number;
  lineHeight: number;
  box: Box;
  outEnd: number; // seconds the title box stays up
};

// Cut-out clip of Juan for one full-screen picture. Its spans are relative to
// srcStart (the clip starts there); outStart is absolute, like the face spans.
export type Matte = { file: string; srcStart: number; srcEnd: number; spans: Span[] };

export type Picture = {
  picture: string;
  show: "card" | "full";
  shot: string;
  box: Box;
  imgW: number;
  imgH: number;
  crop: boolean;
  outStart: number;
  outEnd: number;
  pushed: boolean;
  redact: Box[]; // image pixels
  matte: Matte | null;
};

export type TransparentEdl = {
  format: "transparent";
  fps: number;
  width: number;
  height: number;
  video: string;
  duration: number;
  safe: Box;
  caption: Box;
  spans: Span[];
  title: TitleLayout;
  pictures: Picture[];
  captions: Caption[];
};

export type TransparentProps = TransparentEdl & Record<string, unknown>;

export const toFrame = (seconds: number, fps: number): number => Math.round(seconds * fps);

// Screenshot shows this long after its item's cut (the badge shows on the cut).
export const SHOT_DELAY = 0.2;
