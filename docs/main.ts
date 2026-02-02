import "reveal.js/dist/reset.css";
import "reveal.js/dist/reveal.css";
import "reveal.js/dist/theme/black.css";
import "reveal.js/plugin/highlight/monokai.css";
import "docs/style.css";
import Reveal from "reveal.js";
import Markdown from "reveal.js/plugin/markdown/markdown.esm.js";
import Highlight from "reveal.js/plugin/highlight/highlight.esm.js";
import Notes from "reveal.js/plugin/notes/notes.esm.js";
import Zoom from "reveal.js/plugin/zoom/zoom.esm.js";
import Search from "reveal.js/plugin/search/search.esm.js";
import { slides } from "docs/slides.tsx";

document.querySelector(".reveal")?.replaceChildren(slides());

Reveal.initialize({
  plugins: [Markdown, Highlight, Notes, Zoom, Search],
  markdown: {
    smartypants: true,
  },
  highlight: {
    // Highlight.js options
  },
  slideNumber: true,
  history: true,
  center: true,
  autoPlayMedia: true,
  transitionSpeed: "fast",
});
