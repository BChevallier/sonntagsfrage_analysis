import JSX from "docs/jsx.ts";
import DAX from "analysis/output/line_plots/DAX_Verlauf_dark.svg"
import AfD from "analysis/output/correlations/AfD_vs_DAX_dark.svg"
import CDU_CSU from "analysis/output/correlations/CDU_CSU_vs_DAX_dark.svg"
import FDP from "analysis/output/correlations/FDP_vs_DAX_dark.svg"
import Grüne from "analysis/output/correlations/GRÜNE_vs_DAX_dark.svg"
import Linke from "analysis/output/correlations/LINKE_vs_DAX_dark.svg"
import SPD from "analysis/output/correlations/SPD_vs_DAX_dark.svg"

export function section5() {
  return [
    <section>
      <section>
        <img src={DAX} alt="Verlauf des DAX seit 2000" />
      </section>
      <section>
        <img src={AfD} alt="Korrelation AfD mit DAX" />
      </section>
      <section>
        <img src={CDU_CSU} alt="Korrelation CDU/CSU mit DAX" />
      </section>
      <section>
        <img src={FDP} alt="Korrelation FDP mit DAX" />
      </section>
      <section>
        <img src={Grüne} alt="Korrelation Grüne mit DAX" />
      </section>
      <section>
        <img src={Linke} alt="Korrelation Linke mit DAX" />
      </section>
      <section>
        <img src={SPD} alt="Korrelation SPD mit DAX" />
      </section>
    </section>,
  ];
}
