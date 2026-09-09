import { useCallback, useEffect, useState } from "react";
import { Button } from "../components/ui/Button";
import { DecisionCompassPanel } from "../components/ui/DecisionCompassPanel";
import { DecisionSpectrum } from "../components/ui/DecisionSpectrum";
import { ErrorState } from "../components/ui/ErrorState";
import { LoadingState } from "../components/ui/LoadingState";
import { ProgressIndicator } from "../components/ui/ProgressIndicator";
import { useApp } from "../context/AppContext";
import { fetchDecisionInsight } from "../services/decisionInsightService";
import { toStringList } from "../types";

export function FinalReportScreen() {
  const {
    profile,
    decision,
    analysis,
    scenarios,
    finalReport,
    setFinalReport,
    setScreen,
    resetSession,
    updateDecision,
    invalidateDownstream,
  } = useApp();

  const [loading, setLoading] = useState(!finalReport);
  const [error, setError] = useState<string | null>(null);

  const loadReport = useCallback(async () => {
    if (!profile || !analysis) return;
    setLoading(true);
    setError(null);
    try {
      const report = await fetchDecisionInsight(
        profile,
        decision,
        scenarios,
        analysis,
      );
      setFinalReport(report);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load report.");
    } finally {
      setLoading(false);
    }
  }, [profile, decision, scenarios, analysis, setFinalReport]);

  useEffect(() => {
    if (!profile || !analysis) return;
    if (!finalReport) void loadReport();
  }, [finalReport, profile, analysis, loadReport]);

  if (!profile || !analysis) {
    return (
      <div className="screen view-enter">
        <LoadingState
          title="Preparing your report"
          message="Loading your decision session…"
        />
      </div>
    );
  }

  if (loading) {
    return (
      <div className="screen view-enter">
        <LoadingState
          title="Preparing your decision intelligence"
          message="NUMERA is synthesizing your patterns, context, and options into a clear report…"
        />
      </div>
    );
  }

  if (error || !finalReport) {
    return (
      <div className="screen view-enter">
        <ErrorState
          message={error ?? "Report unavailable."}
          onRetry={() => void loadReport()}
        />
      </div>
    );
  }

  const report = finalReport;
  const compass = report.decision_compass;
  const strongest = report.currently_strongest_option;
  const confidence = report.confidence;
  const whatCouldChange = toStringList(report.what_could_change);
  const numerologyReflection = report.numerology_reflection ?? [];
  const optionAnalysis = report.option_analysis ?? [];
  const keyConsiderations = toStringList(report.key_considerations);
  const nextSteps = toStringList(report.next_steps);
  const derivationNotes = toStringList(report.derivation_notes);

  return (
    <div className="screen screen--report view-enter">
      <ProgressIndicator currentStep={5} />

      <header className="report-masthead">
        <p className="report-masthead__brand">NUMERA</p>
        <h1 className="report-masthead__title">Decision Report</h1>
        <p className="report-masthead__sub">
          A personal brief grounded in what you told NUMERA — not a prediction.
        </p>
        {report.source_label ? (
          <p className="source-banner source-banner--subtle" role="status">
            {report.source_label}
          </p>
        ) : null}
        {report.preview_label ? (
          <p className="dev-banner" role="status">
            {report.preview_label}
          </p>
        ) : null}
      </header>

      <article className="report-doc">
        <section className="report-chapter reveal-stagger" style={{ animationDelay: "0ms" }}>
          <p className="report-chapter__num">01</p>
          <h2 className="report-chapter__title">The decision</h2>
          <p className="report-chapter__caption">What you told NUMERA</p>
          <p className="report-decision-hero">{decision.decision_question}</p>
          <dl className="report-meta-row">
            <div>
              <dt>Focus</dt>
              <dd>{profile.primary_goal}</dd>
            </div>
            {decision.time_horizon ? (
              <div>
                <dt>Time horizon</dt>
                <dd>{decision.time_horizon}</dd>
              </div>
            ) : null}
            {decision.priorities.length > 0 ? (
              <div>
                <dt>Priorities</dt>
                <dd>{decision.priorities.join(", ")}</dd>
              </div>
            ) : null}
          </dl>
        </section>

        <section
          className="report-chapter report-chapter--climax reveal-stagger"
          style={{ animationDelay: "70ms" }}
        >
          <p className="report-chapter__num">02</p>
          <h2 className="report-chapter__title">Decision Compass</h2>
          <p className="report-chapter__caption">What NUMERA shows · Why</p>
          {compass ? (
            <>
              <DecisionSpectrum compass={compass} />
              {strongest && compass.strongest.has_clear_leader ? (
                <div className="compass-leader compass-leader--report">
                  <p className="compass-leader__label">Why it currently stands out</p>
                  <p className="compass-leader__reason">{strongest.reason}</p>
                </div>
              ) : compass.strongest.reason ? (
                <div className="compass-leader compass-leader--report">
                  <p className="compass-leader__label">Why there is no clear leader</p>
                  <p className="compass-leader__reason">{compass.strongest.reason}</p>
                </div>
              ) : null}
              {confidence ? (
                <p className="compass-leader__confidence">
                  Information confidence: {confidence.level} — {confidence.reason}
                </p>
              ) : null}
              <DecisionCompassPanel
                compass={compass}
                showLeader={false}
                hideSpectrum
                hideHeading
              />
            </>
          ) : (
            <p className="report-section__body">Compass unavailable for this session.</p>
          )}
        </section>

        <section className="report-chapter reveal-stagger" style={{ animationDelay: "140ms" }}>
          <p className="report-chapter__num">03</p>
          <h2 className="report-chapter__title">What&apos;s in tension</h2>
          {report.tension_headline ? (
            <p className="tension-headline">
              {report.tension_headline.includes(" vs ")
                ? report.tension_headline.replace(/\s+vs\s+/i, " ↔ ")
                : report.tension_headline}
            </p>
          ) : null}
          <p className="report-prose">{report.key_tension}</p>
        </section>

        <section className="report-chapter reveal-stagger" style={{ animationDelay: "210ms" }}>
          <p className="report-chapter__num">04</p>
          <h2 className="report-chapter__title">Your NUMERA lens</h2>
          <p className="report-chapter__caption">Reflective framework — not a ranking</p>
          {report.numerology_lens_summary ? (
            <p className="report-prose">{report.numerology_lens_summary}</p>
          ) : null}
          <div className="signal-grid">
            {numerologyReflection.map((s, i) => (
              <article
                key={s.signal}
                className="signal-card"
                style={{ animationDelay: `${0.06 * i}s` }}
              >
                <p className="signal-card__label">{s.signal}</p>
                <p className="signal-card__meaning">{s.reflection}</p>
                <p className="signal-card__relevance">
                  {s.numerology_lens || s.decision_relevance}
                </p>
              </article>
            ))}
          </div>
        </section>

        {whatCouldChange.length > 0 ? (
          <section className="report-chapter reveal-stagger" style={{ animationDelay: "280ms" }}>
            <p className="report-chapter__num">05</p>
            <h2 className="report-chapter__title">What could change this</h2>
            <ul className="attention-list">
              {whatCouldChange.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </section>
        ) : null}

        <section className="report-chapter reveal-stagger" style={{ animationDelay: "350ms" }}>
          <p className="report-chapter__num">06</p>
          <h2 className="report-chapter__title">Your next 3 moves</h2>
          <p className="report-chapter__caption">What to do next</p>
          <ol className="steps-list">
            {nextSteps.map((step, i) => (
              <li key={step}>
                <span className="steps-list__num">
                  {String(i + 1).padStart(2, "0")}
                </span>
                <span className="steps-list__text">{step}</span>
              </li>
            ))}
          </ol>
        </section>

        <section
          className="report-chapter report-chapter--wide reveal-stagger"
          style={{ animationDelay: "420ms" }}
        >
          <p className="report-chapter__num">07</p>
          <h2 className="report-chapter__title">The landscape</h2>
          <p className="report-chapter__caption">Option comparison</p>
          <div className="comparison-table-wrap">
            <table className="comparison-table comparison-table--report">
              <thead>
                <tr>
                  <th scope="col">Option</th>
                  <th scope="col">Alignment</th>
                  <th scope="col">Main strength</th>
                  <th scope="col">Main trade-off</th>
                  <th scope="col">Biggest unknown</th>
                </tr>
              </thead>
              <tbody>
                {optionAnalysis.map((opt) => (
                  <tr key={opt.option}>
                    <th scope="row">{opt.option}</th>
                    <td>
                      {opt.numera_alignment
                        ? `${opt.numera_alignment}/100 (${opt.alignment_label ?? ""})`
                        : "—"}
                    </td>
                    <td>{opt.main_strength || opt.upside}</td>
                    <td>{opt.main_tradeoff || opt.tradeoffs}</td>
                    <td>{opt.unknowns}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="report-chapter reveal-stagger" style={{ animationDelay: "490ms" }}>
          <p className="report-chapter__num">08</p>
          <h2 className="report-chapter__title">NUMERA Intelligence</h2>
          <div className="intel-panel">
            <p className="intel-panel__summary">{report.ai_intelligence_summary}</p>
          </div>
          {keyConsiderations.length > 0 ? (
            <>
              <h3 className="report-subhead">What deserves attention</h3>
              <ul className="attention-list">
                {keyConsiderations.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </>
          ) : null}
        </section>

        {derivationNotes.length > 0 ? (
          <section className="report-chapter reveal-stagger" style={{ animationDelay: "560ms" }}>
            <p className="report-chapter__num">09</p>
            <h2 className="report-chapter__title">How this report was derived</h2>
            <ul className="provenance-list">
              {derivationNotes.map((note) => (
                <li key={note}>{note}</li>
              ))}
            </ul>
          </section>
        ) : null}
      </article>

      <p className="legal-disclaimer legal-disclaimer--subtle" role="note">
        NUMERA Alignment reflects how well each option matches the priorities and
        constraints you provided — not a prediction of future outcomes. Numerology is a
        reflective framework, not a scientific prediction.
      </p>

      <div className="form-actions form-actions--report">
        <Button
          onClick={() => {
            invalidateDownstream();
            updateDecision({
              decision_question: "",
              why_considering: "",
              biggest_concern: "",
              context: "",
              user_options: [
                { id: "opt-a", title: "" },
                { id: "opt-b", title: "" },
                { id: "opt-c", title: "" },
              ],
            });
            setScreen("decision");
            window.scrollTo({ top: 0, behavior: "smooth" });
          }}
        >
          Explore another decision →
        </Button>
        <Button variant="secondary" onClick={resetSession}>
          Create a new profile
        </Button>
        <Button variant="ghost" onClick={() => setScreen("what-if")}>
          ← Possibilities
        </Button>
      </div>
    </div>
  );
}
