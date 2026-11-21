// The World, Saturday 21 November 2026.
//
// This program ships the finished front page. The image itself is drawn by
// draw_news.py (Pillow) and committed next to this file as entry.png; all
// this script does is place a copy where the grader looks for it.
//
// Run it from anywhere:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// Inside the grading container MAKEFUN_OUTPUT_DIR is already set, so a
// bare `node main.ts` writes /output/entry.png.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const destination =
  process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const source = join(scriptDir, "entry.png");
if (!existsSync(source)) {
  throw new Error(
    `entry.png is missing next to main.ts (looked in ${scriptDir}); ` +
      "the front page must ship with this program.",
  );
}

mkdirSync(destination, { recursive: true });

const frontPage = readFileSync(source);
const target = join(destination, "entry.png");
writeFileSync(target, frontPage);

console.log(`wrote ${target} (${frontPage.byteLength} bytes)`);
