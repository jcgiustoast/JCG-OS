// Render settings for the short-video editor. make_short.py runs
// `npx remotion render src/index.ts Ranking ...` from this folder.
import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setJpegQuality(92);
Config.setOverwriteOutput(true);
Config.setCodec("h264");
Config.setPixelFormat("yuv420p");
