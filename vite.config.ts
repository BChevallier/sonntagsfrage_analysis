import { defineConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [tsconfigPaths()],
  base: "/revealjs_template/",
  // esbuild: {
  //   jsxFactory: "JSX.createElement",
  //   jsxFragment: "HTMLElement",
  // },
});
