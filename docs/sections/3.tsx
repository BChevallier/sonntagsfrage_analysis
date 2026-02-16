import JSX from "docs/jsx.ts";
import time_correlation from "analysis/output/animations/time_correlation_dark.mp4";

export function section3() {
  return [
    <section>
      <video
        data-src={time_correlation}
        width="800"
        muted
        controls="controls"
      ></video>
    </section>,
  ];
}
