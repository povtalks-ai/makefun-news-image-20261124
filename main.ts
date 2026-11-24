// News-image entry (Node 22, standard library only): the program writes one
// image, the front page drawn for Tuesday 24 November 2026, to
// /output/entry.png. The image is the entry.png beside this file, drawn by
// tools/render.py from the day's researched headlines; this program only
// copies it, so both runs write the same bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

if (!existsSync(source)) {
  throw new Error('entry.png is missing from the repository');
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// The gate only takes a whole PNG or JPEG: refuse to report success unless
// the bytes copied start with the PNG signature.
const head = readFileSync(target).subarray(0, 8);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!head.equals(pngMagic)) {
  throw new Error('entry.png is not a PNG file');
}

const bytes = statSync(target).size;
console.log(`wrote ${target} (${bytes} bytes)`);
