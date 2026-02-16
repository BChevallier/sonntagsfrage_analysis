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
    <section>
      <table>
        <thead>
          <tr>
            <th></th>
            <th>DAX (n=1362)</th>
            <th>VPI (n=312)</th>
            <th>BIP (n=25)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>CDU/CSU</td>
            <td>
              <a href="#/14/2">-0.69</a>
            </td>
            <td>
              <a href="#/12/2">-0.71</a>
            </td>
            <td>
              <a href="#/10/2">-0.69</a>
            </td>
          </tr>
          <tr>
            <td>SPD</td>
            <td>
              <a href="#/14/6">-0.77</a>
            </td>
            <td>
              <a href="#/12/6">-0.79</a>
            </td>
            <td>
              <a href="#/10/6">-0.75</a>
            </td>
          </tr>
          <tr>
            <td>Grüne</td>
            <td>
              <a href="#/14/4">
                <span style="visibility:hidden">-</span>0.28
              </a>
            </td>
            <td>
              <a href="#/12/4">
                <span style="visibility:hidden">-</span>0.38
              </a>
            </td>
            <td>
              <a href="#/10/4">
                <span style="visibility:hidden">-</span>0.45
              </a>
            </td>
          </tr>
          <tr>
            <td>FDP</td>
            <td>
              <a href="#/14/3">-0.27</a>
            </td>
            <td>
              <a href="#/12/3">-0.29</a>
            </td>
            <td>
              <a href="#/10/3">-0.17</a>
            </td>
          </tr>
          <tr>
            <td>Linke</td>
            <td>
              <a href="#/14/5">-0.10</a>
            </td>
            <td>
              <a href="#/12/5">-0.22</a>
            </td>
            <td>
              <a href="#/10/5">-0.39</a>
            </td>
          </tr>
          <tr>
            <td>AfD</td>
            <td>
              <a href="#/14/1">
                <span style="visibility:hidden">-</span>0.84
              </a>
            </td>
            <td>
              <a href="#/12/1">
                <span style="visibility:hidden">-</span>0.82
              </a>
            </td>
            <td>
              <a href="#/10/1">
                <span style="visibility:hidden">-</span>0.81
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </section>,
  ];
}
