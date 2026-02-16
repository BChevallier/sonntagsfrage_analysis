import JSX from "docs/jsx.ts";
import racing_average from "analysis/output/animations/racing_average_dark.mp4";
import growing_average from "analysis/output/animations/sonntagsfrage_rolling_window_dark.mp4";

export function section2() {
  return [
    <section>
      <h2>Datensatz 2</h2>
      2002 - heute
      <br />
      Anzahl Umfragen: 5.079
      <br />
      Quelle: wahlrecht.de
    </section>,
    <section>
      <section>
        <video
          data-src={racing_average}
          width="800"
          muted
        ></video>
      </section>
      <section>
        <video
          data-src={growing_average}
          width="800"
          muted
          controls="controls"
        ></video>
      </section>
    </section>,
  ];
}
