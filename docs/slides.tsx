import JSX from "docs/jsx.ts";
import { section1 } from "docs/sections/1.tsx";
import { section2 } from "docs/sections/2.tsx";
import { section3 } from "docs/sections/3.tsx";
import { section4 } from "docs/sections/4.tsx";
import { section5 } from "docs/sections/5.tsx";

export function slides() {
  return (
    <div class="slides">
      {section1()}
      {section2()}
      {section3()}
      {section4()}
      {section5()}
    </div>
  );
}
