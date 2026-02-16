import JSX from "docs/jsx.ts";
import { section1 } from "docs/sections/1.tsx";
import { section2 } from "docs/sections/2.tsx";
import { section3 } from "docs/sections/3.tsx";
import { section4 } from "docs/sections/4.tsx";
import { sectionDAX } from "docs/sections/5.tsx";
import { sectionBIP } from "docs/sections/6.tsx";
import { sectionVPI } from "docs/sections/7.tsx";

export function slides() {
  return (
    <div class="slides">
      {section1()}
      {section2()}
      {section3()}
      {section4()}
      {sectionBIP()}
      {sectionVPI()}
      {sectionDAX()}
    </div>
  );
}
