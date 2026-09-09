import { Button } from "../components/ui/Button";
import { DirectionCard } from "../components/ui/DirectionCard";
import { ProgressIndicator } from "../components/ui/ProgressIndicator";
import { SectionHeading } from "../components/ui/SectionHeading";
import { useApp } from "../context/AppContext";
import { toStringList } from "../types";
import type { PossibleDirection } from "../types";

function toDirectionCard(opt: {
  id: string;
  label: string;
  title: string;
  upside: string;
  tradeoff: string;
  questions: string[];
}): PossibleDirection {
  return {
    id: opt.id,
    label: opt.label,
    title: opt.title,
    upside: opt.upside,
    tradeoff: opt.tradeoff,
    questions: opt.questions,
  };
}

function sourceBadge(source: string): string {
  if (source === "user") return "Your option";
  if (source === "user_custom") return "Custom path";
  return "Suggested path";
}

function formatTension(headline: string): string {
  if (headline.includes("↔")) return headline;
  if (headline.includes(" vs ")) return headline.replace(/\s+vs\s+/i, " ↔ ");
  return headline;
}

export function DecisionIntelligenceScreen() {
  const { profile, decision, analysis, setScreen } = useApp();

  if (!profile || !analysis) return null;

  const decisionQuestions = toStringList(analysis.decision_questions);
  const considerations = toStringList(analysis.considerations);
  const options = analysis.options ?? [];

  return (
    <div className="screen view-enter">
      <ProgressIndicator currentStep={3} />

      <SectionHeading
        eyebrow="Step 03 · Understand"
        title="Your decision intelligence"
        subtitle="Structured reflection from your inputs and numerology signals — not a prediction."
      />

      {analysis.source_label ? (
        <p className="source-banner source-banner--subtle" role="status">
          {analysis.source_label}
        </p>
      ) : null}
      {analysis.preview_label ? (
        <p className="dev-banner" role="status">
          {analysis.preview_label}
        </p>
      ) : null}

      <section className="intel-story" aria-labelledby="your-decision-heading">
        <p className="intel-story__num">01</p>
        <h2 id="your-decision-heading" className="intel-story__title">
          Your decision
        </h2>
        <p className="intel-story__caption">What you told NUMERA</p>
        <blockquote className="decision-quote">
          &ldquo;{decision.decision_question}&rdquo;
        </blockquote>
        {analysis.summary ? (
          <p className="intel-story__body">{analysis.summary}</p>
        ) : null}
      </section>

      <section className="intel-story intel-story--tension" aria-labelledby="tension-heading">
        <p className="intel-story__num">02</p>
        <h2 id="tension-heading" className="intel-story__title">
          What&apos;s really in tension?
        </h2>
        <p className="intel-story__caption">What NUMERA understood</p>
        {analysis.tension_headline ? (
          <p className="tension-headline">
            {formatTension(analysis.tension_headline)}
          </p>
        ) : null}
        <p className="intel-section__body">{analysis.key_tension}</p>
        {analysis.decision_synthesis !== analysis.key_tension ? (
          <p className="intel-section__body">{analysis.decision_synthesis}</p>
        ) : null}
      </section>

      <section className="intel-story" aria-labelledby="signals-heading">
        <p className="intel-story__num">03</p>
        <h2 id="signals-heading" className="intel-story__title">
          Your NUMERA signals
        </h2>
        <p className="intel-story__caption">What NUMERA shows — reflective lens</p>
        <div className="signal-grid">
          {analysis.contextual_signals.map((s, i) => (
            <article
              key={s.signal}
              className="signal-card signal-card--structured reveal-stagger"
              style={{ animationDelay: `${0.07 * i}s` }}
            >
              <p className="signal-card__eyebrow">Number</p>
              <p className="signal-card__label">{s.signal}</p>
              <p className="signal-card__theme">
                <span className="signal-card__theme-label">Traditional theme</span>
                {s.traditional_theme}
              </p>
              <p className="signal-card__why">
                <span className="signal-card__theme-label">Why it matters here</span>
                {s.why_it_matters_here || s.decision_relevance}
              </p>
              <p className="signal-card__meaning">
                <span className="signal-card__theme-label">Reflection</span>
                {s.reflection}
              </p>
            </article>
          ))}
        </div>
      </section>

      {decisionQuestions.length > 0 ? (
        <section className="intel-section" aria-labelledby="questions-heading">
          <h2 id="questions-heading" className="intel-section__title">
            Questions to investigate
          </h2>
          <ul className="considerations-list">
            {decisionQuestions.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </section>
      ) : null}

      <section className="intel-section" aria-labelledby="alignment-heading">
        <h2 id="alignment-heading" className="intel-section__title">
          Goal alignment
        </h2>
        <p className="intel-section__body">{analysis.goal_alignment}</p>
      </section>

      <section className="intel-section" aria-labelledby="directions-heading">
        <h2 id="directions-heading" className="intel-section__title">
          Possible directions
        </h2>
        <p className="intel-section__intro">
          Options connected to your {decision.decision_area.toLowerCase()} decision —
          compare trade-offs, not predicted outcomes.
        </p>
        <div className="direction-grid">
          {options.map((d, i) => (
            <div key={d.id} className="direction-card-wrap">
              <span className="option-source-badge">{sourceBadge(d.source)}</span>
              <DirectionCard direction={toDirectionCard(d)} delay={0.08 * i} />
            </div>
          ))}
        </div>
      </section>

      <section className="intel-section" aria-labelledby="considerations-heading">
        <h2 id="considerations-heading" className="intel-section__title">
          What deserves your attention
        </h2>
        <ul className="considerations-list">
          {considerations.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>

      <p className="legal-disclaimer" role="note">
        NUMERA provides structured reflection and AI-assisted analysis, not guaranteed
        predictions or professional advice.
      </p>

      <div className="form-actions">
        <Button onClick={() => setScreen("what-if")}>Explore possibilities →</Button>
        <Button variant="ghost" onClick={() => setScreen("decision")}>
          Refine my decision
        </Button>
      </div>
    </div>
  );
}
