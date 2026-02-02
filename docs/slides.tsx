import JSX from "docs/jsx.ts";
import { reference } from "docs/sections/reference.tsx";

export function slides() {
  return <div class="slides">{reference()}</div>;
}
