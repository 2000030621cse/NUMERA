import { FormEvent, useState } from "react";
import { Button } from "../components/ui/Button";
import { ChipSelect } from "../components/ui/ChipSelect";
import { ProgressIndicator } from "../components/ui/ProgressIndicator";
import { SectionHeading } from "../components/ui/SectionHeading";
import { Select } from "../components/ui/Select";
import { Input } from "../components/ui/Input";
import { LoadingState } from "../components/ui/LoadingState";
import { ErrorState } from "../components/ui/ErrorState";
import { useApp } from "../context/AppContext";
import { analyzeDecision } from "../services/decisionService";
import {
  PRIMARY_GOALS,
  PRIORITIES,
  RISK_TOLERANCES,
  TIME_HORIZONS,
  type DecisionArea,
  type Priority,
  type RiskTolerance,
  type TimeHorizon,
} from "../types";

const OPTION_LABELS = ["Option A", "Option B", "Option C"] as const;
const OPTION_HINTS = [
  "e.g. Stay in my current role",
  "e.g. Switch to a new company",
  "e.g. Prepare while staying",
] as const;

export function DecisionExplorationScreen() {
  const { profile, decision, updateDecision, commitAnalysisResult, setScreen } =
    useApp();
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [formError, setFormError] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showDetails, setShowDetails] = useState(false);

  if (!profile) return null;
  const activeProfile = profile;

  function validate() {
    const next: Record<string, string> = {};
    if (!decision.decision_question.trim()) {
      next.decision_question = "Describe the decision you're trying to make.";
    }
    if (decision.priorities.length === 0) {
      next.priorities = "Select at least one priority.";
    }
    const filledOptions = (decision.user_options ?? []).filter((o) =>
      o.title.trim(),
    );
    if (filledOptions.length < 2) {
      next.user_options = "Enter at least two paths you are considering.";
    }
    return next;
  }

  function updateOption(index: number, title: string) {
    const next = (decision.user_options ?? []).map((o, i) =>
      i === index ? { ...o, title } : o,
    );
    updateDecision({ user_options: next });
    setErrors((p) => ({ ...p, user_options: "" }));
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setFormError(null);
    const nextErrors = validate();
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) return;

    setIsAnalyzing(true);
    try {
      const result = await analyzeDecision({ profile: activeProfile, decision });
      commitAnalysisResult(result);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      setFormError(
        err instanceof Error ? err.message : "Analysis failed. Please try again.",
      );
    } finally {
      setIsAnalyzing(false);
    }
  }

  if (isAnalyzing) {
    return (
      <div className="screen view-enter">
        <LoadingState
          title="Understanding your decision"
          message="NUMERA is connecting your personal patterns with your specific situation…"
        />
      </div>
    );
  }

  return (
    <div className="screen view-enter">
      <ProgressIndicator currentStep={2} />
      <SectionHeading
        eyebrow="Step 02 · Frame"
        title="Let's frame the decision clearly"
        subtitle="Your actual decision is the focal point. Options you define here drive Possibilities and your Decision Report."
      />

      <form className="panel-form panel-form--decision" onSubmit={handleSubmit} noValidate>
        <section className="form-chapter" aria-labelledby="decision-hero-label">
          <p id="decision-hero-label" className="form-chapter__label">
            Your decision
          </p>
          <label className="field field--hero">
            <span className="field-label">What decision are you trying to make?</span>
            <textarea
              className="field-control field-control--textarea field-control--hero"
              name="decision_question"
              rows={3}
              placeholder="Should I switch to a new company this year?"
              value={decision.decision_question}
              onChange={(e) => {
                updateDecision({ decision_question: e.target.value });
                setErrors((p) => ({ ...p, decision_question: "" }));
              }}
              aria-invalid={Boolean(errors.decision_question)}
            />
            {errors.decision_question ? (
              <span className="field-error" role="alert">
                {errors.decision_question}
              </span>
            ) : (
              <span className="field-hint">
                Be specific — this anchors everything that follows.
              </span>
            )}
          </label>

          <Select
            label="Decision area"
            name="decision_area"
            value={decision.decision_area}
            onChange={(e) =>
              updateDecision({ decision_area: e.target.value as DecisionArea })
            }
            options={PRIMARY_GOALS.map((g) => ({ value: g, label: g }))}
          />
        </section>

        <section className="form-chapter" aria-labelledby="priorities-label">
          <p id="priorities-label" className="form-chapter__label">
            Priorities & timing
          </p>
          <ChipSelect
            label="What matters most to you?"
            options={PRIORITIES}
            selected={decision.priorities}
            onChange={(priorities) => {
              updateDecision({ priorities: priorities as Priority[] });
              setErrors((p) => ({ ...p, priorities: "" }));
            }}
            hint="Select all that apply — these weight Decision Compass."
            error={errors.priorities}
          />
          <Select
            label="How soon do you need to decide?"
            name="time_horizon"
            placeholder="Select a time horizon"
            value={decision.time_horizon}
            onChange={(e) =>
              updateDecision({ time_horizon: e.target.value as TimeHorizon | "" })
            }
            options={TIME_HORIZONS.map((h) => ({ value: h, label: h }))}
          />
        </section>

        <section className="form-chapter" aria-labelledby="options-label">
          <p id="options-label" className="form-chapter__label">
            Your paths
          </p>
          <p className="field-hint form-chapter__hint">
            Enter at least two options. These are the paths Decision Compass will compare.
          </p>
          <div className="option-input-grid">
            {OPTION_LABELS.map((label, index) => (
              <div key={decision.user_options[index]?.id ?? label} className="option-input-card">
                <span className="option-source-badge">Your option</span>
                <Input
                  label={index < 2 ? `${label} *` : `${label} (optional)`}
                  name={`user_option_${index}`}
                  placeholder={OPTION_HINTS[index]}
                  value={decision.user_options[index]?.title ?? ""}
                  onChange={(e) => updateOption(index, e.target.value)}
                />
              </div>
            ))}
          </div>
          {errors.user_options ? (
            <span className="field-error" role="alert">
              {errors.user_options}
            </span>
          ) : null}
        </section>

        {!showDetails ? (
          <Button variant="ghost" type="button" onClick={() => setShowDetails(true)}>
            + Add more context (optional)
          </Button>
        ) : (
          <section className="form-chapter" aria-labelledby="context-label">
            <p id="context-label" className="form-chapter__label">
              Additional context
            </p>
            <label className="field">
              <span className="field-label">Why are you considering this?</span>
              <textarea
                className="field-control field-control--textarea"
                rows={3}
                placeholder="I feel stagnant and a new opportunity appeared…"
                value={decision.why_considering}
                onChange={(e) => updateDecision({ why_considering: e.target.value })}
              />
            </label>
            <Input
              label="What is your biggest concern?"
              name="biggest_concern"
              placeholder="e.g. Leaving a stable team"
              value={decision.biggest_concern}
              onChange={(e) => updateDecision({ biggest_concern: e.target.value })}
            />
            <label className="field">
              <span className="field-label">Constraints or limitations</span>
              <textarea
                className="field-control field-control--textarea"
                rows={2}
                placeholder="Financial obligations, location, family responsibilities…"
                value={decision.constraints}
                onChange={(e) => updateDecision({ constraints: e.target.value })}
              />
            </label>
            <Select
              label="Risk tolerance"
              name="risk_tolerance"
              placeholder="How much uncertainty can you accept?"
              value={decision.risk_tolerance}
              onChange={(e) =>
                updateDecision({
                  risk_tolerance: e.target.value as RiskTolerance | "",
                })
              }
              options={RISK_TOLERANCES.map((r) => ({ value: r, label: r }))}
            />
            <label className="field">
              <span className="field-label">Anything else?</span>
              <textarea
                className="field-control field-control--textarea"
                rows={3}
                placeholder="Anything else NUMERA should know about your situation…"
                value={decision.context}
                onChange={(e) => updateDecision({ context: e.target.value })}
              />
            </label>
          </section>
        )}

        {formError ? <ErrorState message={formError} /> : null}

        <div className="form-actions">
          <Button type="submit">Analyze my decision →</Button>
          <Button
            variant="ghost"
            type="button"
            onClick={() => setScreen("profile-results")}
          >
            ← Back to profile
          </Button>
        </div>
      </form>
    </div>
  );
}
