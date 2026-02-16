import JSX from "docs/jsx.ts";
import VPI from "analysis/output/line_plots/VPI_Verlauf_dark.svg";
import AfD from "analysis/output/correlations/AfD_vs_VPI_dark.svg";
import CDU_CSU from "analysis/output/correlations/CDU_CSU_vs_VPI_dark.svg";
import FDP from "analysis/output/correlations/FDP_vs_VPI_dark.svg";
import Grüne from "analysis/output/correlations/GRÜNE_vs_VPI_dark.svg";
import Linke from "analysis/output/correlations/LINKE_vs_VPI_dark.svg";
import SPD from "analysis/output/correlations/SPD_vs_VPI_dark.svg";

export function sectionVPI() {
  return [
    <section>
      <h2>Datensatz 4</h2>
      2000 - heute
      <br />
      monatlicher VPI (n=312)
      <br />
      Quelle: destatits.de
    </section>,
    <section>
      <section>
        <img src={VPI} alt="Verlauf des VPI seit 2000" />
      </section>
      <section>
        <img src={AfD} alt="Korrelation AfD mit VPI" />
      </section>
      <section>
        <img src={CDU_CSU} alt="Korrelation CDU/CSU mit VPI" />
      </section>
      <section>
        <img src={FDP} alt="Korrelation FDP mit VPI" />
      </section>
      <section>
        <img src={Grüne} alt="Korrelation Grüne mit VPI" />
      </section>
      <section>
        <img src={Linke} alt="Korrelation Linke mit VPI" />
      </section>
      <section>
        <img src={SPD} alt="Korrelation SPD mit VPI" />
      </section>
    </section>,
  ];
}
