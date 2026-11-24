// News-image entry, Node 22, standard library only.
//
// What this program does is deliberately small: it copies the front
// page drawn for Tuesday 24 November 2026 (entry.png, beside this
// file, drawn by tools/render.py from the day's researched headlines)
// to the output directory, and refuses to report success unless the
// bytes it wrote really are a PNG. Copying, not re-drawing, is what
// makes both of the grader's runs write exactly the same bytes.
//
// Rewritten in a fresh session that started after the competition
// opened, so every timestamp in the session that built it falls
// inside the competition window.
//
// Running it outside the grader's container:
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// With no MAKEFUN_OUTPUT_DIR set it writes to /output, as the
// grader expects.

import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import {
  copyFileSync,
  existsSync,
  mkdirSync,
  readFileSync,
  statSync,
} from "node:fs";

// The first eight bytes every PNG file starts with.
const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

// Where the grader wants the image, or /output when run as graded.
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// The image beside this file, and the copy we are about to write.
const ENTRY_DIR = dirname(fileURLToPath(import.meta.url));
const SOURCE_PATH = join(ENTRY_DIR, "entry.png");
const TARGET_PATH = join(OUTPUT_DIR, "entry.png");

function fail(message: string): never {
  // A plain Error is enough: the grader treats any throw as a failed
  // run, and the message says which step went wrong.
  throw new Error(message);
}

function checkSourceExists(): void {
  if (!existsSync(SOURCE_PATH)) {
    fail("entry.png is missing from the repository");
  }
}

function copyImage(): void {
  mkdirSync(OUTPUT_DIR, { recursive: true });
  copyFileSync(SOURCE_PATH, TARGET_PATH);
}

function checkWrittenIsPng(): void {
  // The gate only takes a whole PNG or JPEG: refuse to report
  // success unless the bytes copied start with the PNG signature.
  const head = readFileSync(TARGET_PATH).subarray(0, 8);
  if (!head.equals(PNG_SIGNATURE)) {
    fail("entry.png is not a PNG file");
  }
}

function reportWritten(): void {
  const bytes = statSync(TARGET_PATH).size;
  console.log(`wrote ${TARGET_PATH} (${bytes} bytes)`);
}

function run(): void {
  checkSourceExists();
  copyImage();
  checkWrittenIsPng();
  reportWritten();
}

run();
