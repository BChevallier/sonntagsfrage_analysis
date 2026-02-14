import { defineConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [tsconfigPaths()],
  base: "/sonntagsfrage_analysis/",
  // esbuild: {
  //   jsxFactory: "JSX.createElement",
  //   jsxFragment: "HTMLElement",
  // },
});
