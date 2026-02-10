import JSX from "docs/jsx.ts";
import Umfragezahl_pro_Institution from "analysis/output/histograms/Umfrageanzahl_pro_Institut_dark.svg";
import Umfragezahl_pro_Wahl from "analysis/output/histograms/Umfrageanzahl_pro_Wahl_dark.svg";

export function section1() {
  return [
    <section>
      <h3>Umfrageinstitute, analysiert</h3>
      <p>
        <small>von Bastien Chevallier und Johannes Frohnmeyer</small>
      </p>
    </section>,
    <section
      data-auto-animate
      data-auto-animate-easing="cubic-bezier(0.770, 0.000, 0.175, 1.000)"
    >
      <blockquote>
        &ldquo;Wenn am nächsten Sonntag wirklich Bundestagswahl wäre, welche der
        folgenden Parteien würden Sie dann wählen?&rdquo;
      </blockquote>
    </section>,
    <section>
      <h2>Datensatz 1</h2>
      2017 - heute
      <br />
      Anzahl Umfragen: 3.700
      <br />
      Quelle: dawum.de
    </section>,
    <section>
      <div style="display: flex; gap: 1rem; justifyContent: center; alignItems: center">
        <img
          src={Umfragezahl_pro_Institution}
          alt="Umfrageanzahl pro Institut"
          style="max-width: 48%; height: auto;"
        />
        <img
          src={Umfragezahl_pro_Wahl}
          alt="Umfrageanzahl pro Wahl"
          style="max-width: 48%; height: auto;"
        />
      </div>
    </section>,
  ];
}
