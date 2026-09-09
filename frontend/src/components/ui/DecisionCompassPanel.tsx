import type { DecisionCompass } from "../../types";
import { DecisionSpectrum } from "./DecisionSpectrum";

type DecisionCompassPanelProps = {
  compass: DecisionCompass;
  showLeader?: boolean;
  /** Hide detailed score cards (spectrum + status only) */
  spectrumOnly?: boolean;
  /** When spectrum is already rendered above (e.g. report climax) */
  hideSpectrum?: boolean;
  /** Omit the section heading (parent already titled the chapter) */
  hideHeading?: boolean;
};

export function DecisionCompassPanel({
  compass,
  showLeader = true,
  spectrumOnly = false,
  hideSpectrum = false,
  hideHeading = false,
}: DecisionCompassPanelProps) {
  const { strongest, confidence, scores } = compass;

  return (
    <section
      className={`compass-panel${hideHeading ? " compass-panel--embedded" : ""}`}
      aria-labelledby={hideHeading ? undefined : "compass-heading"}
    >
      {!hideHeading ? (
        <>
          <h2 id="compass-heading" className="intel-section__title">
            Decision Compass
          </h2>
          <p className="compass-panel__intro">
            Alignment with what you told NUMERA — priorities, constraints, concern, and
            time horizon.
          </p>
        </>
      ) : null}
      <p className="compass-panel__note">{compass.transparency_note}</p>
      <p className="compass-panel__note compass-panel__note--subtle">
        {compass.numerology_note}
      </p>

      {!hideSpectrum ? <DecisionSpectrum compass={compass} /> : null}

      {showLeader ? (
        <div className="compass-leader">
          <p className="compass-leader__label">
            {strongest.has_clear_leader
              ? "Currently strongest alignment"
              : "No clear leader yet"}
          </p>
          <p className="compass-leader__title">
            {strongest.has_clear_leader ? strongest.title : "Options are closely matched"}
          </p>
          <p className="compass-leader__reason">{strongest.reason}</p>
          <p className="compass-leader__confidence">
            Information confidence: {confidence.level} — {confidence.reason}
          </p>
        </div>
      ) : null}

      {!spectrumOnly ? (
        <div className="compass-grid">
          {scores.map((score) => (
            <article key={score.option_id} className="compass-card">
              <div className="compass-card__header">
                <h3 className="compass-card__title">{score.option_title}</h3>
                <p className="compass-card__score">
                  NUMERA Alignment: <strong>{score.numera_alignment}</strong>/100
                </p>
                <p className="compass-card__label">{score.alignment_label}</p>
              </div>
              <dl className="compass-card__dl">
                <div>
                  <dt>Priority fit</dt>
                  <dd>{score.breakdown.priority_score}/100</dd>
                </div>
                <div>
                  <dt>Risk fit</dt>
                  <dd>{score.breakdown.risk_score}/100</dd>
                </div>
                <div>
                  <dt>Constraint fit</dt>
                  <dd>{score.breakdown.constraint_score}/100</dd>
                </div>
                <div>
                  <dt>Time-horizon fit</dt>
                  <dd>{score.breakdown.time_horizon_score}/100</dd>
                </div>
                <div>
                  <dt>Strengths</dt>
                  <dd>{score.strengths}</dd>
                </div>
                <div>
                  <dt>Trade-offs</dt>
                  <dd>{score.tradeoffs}</dd>
                </div>
                <div>
                  <dt>Unknowns</dt>
                  <dd>{score.unknowns}</dd>
                </div>
              </dl>
              {score.evidence_to_check.length > 0 ? (
                <div className="compass-card__evidence">
                  <p className="compass-card__evidence-label">Evidence to check</p>
                  <ul>
                    {score.evidence_to_check.map((e) => (
                      <li key={e}>{e}</li>
                    ))}
                  </ul>
                </div>
              ) : null}
            </article>
          ))}
        </div>
      ) : null}

      {compass.what_could_change.length > 0 && showLeader ? (
        <div className="compass-change">
          <h3 className="compass-change__title">What could change this assessment</h3>
          <ul className="attention-list">
            {compass.what_could_change.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      ) : null}

      <p className="compass-panel__formula">{compass.scoring_formula}</p>
    </section>
  );
}
