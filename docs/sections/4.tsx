import JSX from "docs/jsx.ts";
import ALLEN_bias from "analysis/output/survey_deviations/Allensberger_dark.svg";
import FORSA_bias from "analysis/output/survey_deviations/Forsa_dark.svg";
import FOWA_bias from "analysis/output/survey_deviations/Forsch'gr. Wahlen_dark.svg";
import GMS_bias from "analysis/output/survey_deviations/GMS_dark.svg";
import INFRA_bias from "analysis/output/survey_deviations/Infratest dimap_dark.svg";
import INSA_bias from "analysis/output/survey_deviations/INSA_dark.svg";
import VERIAN_bias from "analysis/output/survey_deviations/Verian (Emnid)_dark.svg";
import YOUGOV_bias from "analysis/output/survey_deviations/YouGov_dark.svg";


export function section4() {
  return [
    <section>
      <section>
        <img src={ALLEN_bias} alt="Biasanalyse Allensberger" />
      </section>
      <section>
        <img src={FORSA_bias} alt="Biasanalyse Forsa" />
      </section>
      <section>
        <img src={FOWA_bias} alt="Biasanalyse FoWA" />
      </section>
      <section>
        <img src={GMS_bias} alt="Biasanalyse GMS" />
      </section>
      <section>
        <img src={INFRA_bias} alt="Biasanalyse Infra" />
      </section>
      <section>
        <img src={INSA_bias} alt="Biasanalyse INSA" />
      </section>
      <section>
        <img src={VERIAN_bias} alt="Biasanalyse Verian" />
      </section>
      <section>
        <img src={YOUGOV_bias} alt="Biasanalyse YouGov" />
      </section>
    </section>,
  ];
}
