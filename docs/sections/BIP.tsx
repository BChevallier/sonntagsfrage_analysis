import JSX from "docs/jsx.ts";
import BIP from "analysis/output/line_plots/BIP_Verlauf_dark.svg";
import AfD from "analysis/output/correlations/AfD_vs_BIP_dark.svg";
import CDU_CSU from "analysis/output/correlations/CDU_CSU_vs_BIP_dark.svg";
import FDP from "analysis/output/correlations/FDP_vs_BIP_dark.svg";
import Grüne from "analysis/output/correlations/GRÜNE_vs_BIP_dark.svg";
import Linke from "analysis/output/correlations/LINKE_vs_BIP_dark.svg";
import SPD from "analysis/output/correlations/SPD_vs_BIP_dark.svg";

export function sectionBIP() {
  return [
    <section>
      <h2>Datensatz 3</h2>
      2000 - heute
      <br />
      jährliches BIP (n=25)
      <br />
      Quelle: destatis.de
    </section>,
    <section>
      <section>
        <img src={BIP} alt="Verlauf des DAX seit 2000" />
      </section>
      <section>
        <img src={AfD} alt="Korrelation AfD mit BIP" />
      </section>
      <section>
        <img src={CDU_CSU} alt="Korrelation CDU/CSU mit BIP" />
      </section>
      <section>
        <img src={FDP} alt="Korrelation FDP mit BIP" />
      </section>
      <section>
        <img src={Grüne} alt="Korrelation Grüne mit BIP" />
      </section>
      <section>
        <img src={Linke} alt="Korrelation Linke mit BIP" />
      </section>
      <section>
        <img src={SPD} alt="Korrelation SPD mit BIP" />
      </section>
    </section>,
  ];
}
