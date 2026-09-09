import { useEffect, useState } from "react";
import { Button } from "../components/ui/Button";
import { DecisionCompassPanel } from "../components/ui/DecisionCompassPanel";
import { ProgressIndicator } from "../components/ui/ProgressIndicator";
import { SectionHeading } from "../components/ui/SectionHeading";
import { useApp } from "../context/AppContext";
import { fetchDecisionCompass } from "../services/compassService";
import type { DecisionCompass, WhatIfScenario } from "../types";



function sourceBadge(source: string): string {

  if (source === "user") return "Your option";

  if (source === "user_custom") return "Custom path";

  return "Suggested path";

}



export function WhatIfScreen() {
  const { profile, decision, scenarios, setScenarios, setScreen, setFinalReport, analysis } =
    useApp();
  const [showComparison, setShowComparison] = useState(false);
  const [customName, setCustomName] = useState("");
  const [compass, setCompass] = useState<DecisionCompass | null>(
    analysis?.decision_compass ?? null,
  );
  const [compassLoading, setCompassLoading] = useState(false);

  useEffect(() => {
    if (!profile || scenarios.length === 0) return;
    let cancelled = false;
    setCompassLoading(true);
    fetchDecisionCompass(profile, decision, scenarios)
      .then((result) => {
        if (!cancelled) setCompass(result);
      })
      .catch(() => {
        if (!cancelled && analysis?.decision_compass) {
          setCompass(analysis.decision_compass);
        }
      })
      .finally(() => {
        if (!cancelled) setCompassLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [profile, decision, scenarios, analysis?.decision_compass]);



  function addScenario() {

    if (!customName.trim()) return;

    const id = `custom-${Date.now()}`;

    const title = customName.trim();

    const next: WhatIfScenario = {

      id,

      label: "Custom",

      title,

      source: "user_custom",

      name: title.toUpperCase(),

      assumption: title,

      upside: `Potential benefit if "${title}" fits your priorities for: "${decision.decision_question.slice(0, 80)}".`,

      tradeoff: `Trade-offs depend on how this path affects your concern${decision.biggest_concern ? `: "${decision.biggest_concern}"` : " and constraints"}.`,

      uncertainty: "What evidence would confirm or reject this path?",

      reversibility: "Assess based on how reversible this choice would be in your situation.",

      alignment: decision.priorities.length > 0 ? `Compare against: ${decision.priorities.join(", ")}` : "—",

      questions: [

        `How does "${title}" address your decision?`,

        "What would need to be true for this scenario to work?",

      ],

      evidence_to_check: [

        "Identify one fact that would confirm or reject this path.",

      ],

      expected_benefit: `Potential benefit if "${title}" fits your stated priorities.`,

      possible_tradeoff: "Define what you might give up or risk on this path.",

    };

    setScenarios([...scenarios, next]);

    setCustomName("");

  }



  if (scenarios.length === 0) return null;



  return (

    <div className="screen view-enter">

      <ProgressIndicator currentStep={4} />



      <SectionHeading
        eyebrow="Step 04 · Explore"
        title="Explore your possibilities"
        subtitle="There isn't necessarily one answer. Compare every path, then see how each aligns with what you told NUMERA."
      />



      <blockquote className="decision-quote decision-quote--compact">

        &ldquo;{decision.decision_question}&rdquo;

      </blockquote>



      <div className="scenario-grid">

        {scenarios.map((scenario, i) => (

          <article

            key={scenario.id}

            className="scenario-card"

            style={{ animationDelay: `${0.07 * i}s` }}

          >

            <p className="option-source-badge option-source-badge--card">

              {sourceBadge(scenario.source)}

            </p>

            <h2 className="scenario-card__name">{scenario.label}: {scenario.title}</h2>

            <div className="scenario-card__block">

              <p className="scenario-card__label">Potential benefit</p>

              <p>{scenario.upside}</p>

            </div>

            <div className="scenario-card__block">

              <p className="scenario-card__label">Trade-off</p>

              <p>{scenario.tradeoff}</p>

            </div>

            <div className="scenario-card__block">

              <p className="scenario-card__label">Uncertainty</p>

              <p>{scenario.uncertainty}</p>

            </div>

            <div className="scenario-card__block">

              <p className="scenario-card__label">Reversibility</p>

              <p>{scenario.reversibility}</p>

            </div>

            <div className="scenario-card__block">

              <p className="scenario-card__label">Alignment with priorities</p>

              <p>{scenario.alignment}</p>

            </div>

            <div className="scenario-card__block">

              <p className="scenario-card__label">Questions to investigate</p>

              <ul>

                {scenario.questions.map((q) => (

                  <li key={q}>{q}</li>

                ))}

              </ul>

            </div>

          </article>

        ))}

      </div>

      {compassLoading ? (
        <p className="compass-panel__loading" role="status">Calculating Decision Compass…</p>
      ) : compass ? (
        <DecisionCompassPanel compass={compass} />
      ) : null}

      <div className="custom-scenario">

        <label className="field">

          <span className="field-label">Add a custom path</span>

          <input

            className="field-control"

            type="text"

            placeholder="What if I…"

            value={customName}

            onChange={(e) => setCustomName(e.target.value)}

            onKeyDown={(e) => {

              if (e.key === "Enter") {

                e.preventDefault();

                addScenario();

              }

            }}

          />

        </label>

        <Button variant="secondary" onClick={addScenario}>

          Add path

        </Button>

      </div>



      <div className="form-actions">

        <Button

          onClick={() => {

            setFinalReport(null);

            setScreen("final-report");

            window.scrollTo({ top: 0, behavior: "smooth" });

          }}

        >

          View final report →

        </Button>

        <Button onClick={() => setShowComparison(true)}>

          Compare scenarios

        </Button>

        <Button variant="ghost" onClick={() => setScreen("intelligence")}>

          ← Back to decision intelligence

        </Button>

      </div>



      {showComparison ? (

        <section className="comparison view-enter" aria-labelledby="comparison-heading">

          <h2 id="comparison-heading" className="comparison__title">

            Scenario comparison

          </h2>

          <p className="comparison__note">

            Structured exploration for &ldquo;{decision.decision_question}&rdquo; —

            compare assumptions, not futures.

          </p>

          <div className="comparison-table-wrap">

            <table className="comparison-table">

              <thead>

                <tr>

                  <th scope="col">Dimension</th>

                  {scenarios.map((s) => (

                    <th key={s.id} scope="col">{s.title}</th>

                  ))}

                </tr>

              </thead>

              <tbody>

                <tr>

                  <th scope="row">Benefit</th>

                  {scenarios.map((s) => (

                    <td key={`${s.id}-ben`}>{s.upside}</td>

                  ))}

                </tr>

                <tr>

                  <th scope="row">Trade-off</th>

                  {scenarios.map((s) => (

                    <td key={`${s.id}-trade`}>{s.tradeoff}</td>

                  ))}

                </tr>

                <tr>

                  <th scope="row">Uncertainty</th>

                  {scenarios.map((s) => (

                    <td key={`${s.id}-unc`}>{s.uncertainty}</td>

                  ))}

                </tr>

                <tr>

                  <th scope="row">Reversibility</th>

                  {scenarios.map((s) => (

                    <td key={`${s.id}-rev`}>{s.reversibility}</td>

                  ))}

                </tr>

                <tr>

                  <th scope="row">Alignment</th>

                  {scenarios.map((s) => (

                    <td key={`${s.id}-align`}>{s.alignment}</td>

                  ))}

                </tr>

                <tr>

                  <th scope="row">Evidence to check</th>

                  {scenarios.map((s) => (

                    <td key={`${s.id}-ev`}>

                      <ul className="comparison-questions">

                        {s.evidence_to_check.map((e) => (

                          <li key={e}>{e}</li>

                        ))}

                      </ul>

                    </td>

                  ))}

                </tr>

              </tbody>

            </table>

          </div>

        </section>

      ) : null}

    </div>

  );

}

