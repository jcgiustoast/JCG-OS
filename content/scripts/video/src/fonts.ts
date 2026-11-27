// Juan's brand fonts, imported straight from the visual engine's folder
// (no copies). Remotion's bundler turns these imports into asset URLs, and
// loadFont holds the render until each font is ready.
import { loadFont } from "@remotion/fonts";
import archimotoMedium from "../../visual/assets/fonts/archimoto-medium.otf";
import archivoMedium from "../../visual/assets/fonts/archivo-medium.ttf";
import bigShouldersExtraBold from "../../visual/assets/fonts/bigshoulders-extrabold.ttf";

export const BADGE_FONT = "Archimoto";
export const CAPTION_FONT = "Archivo";
export const TITLE_FONT = "Big Shoulders";

loadFont({ family: BADGE_FONT, url: archimotoMedium, weight: "500" });
loadFont({ family: CAPTION_FONT, url: archivoMedium, weight: "500" });
loadFont({ family: TITLE_FONT, url: bigShouldersExtraBold, weight: "800" });
