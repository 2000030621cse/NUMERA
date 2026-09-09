import { Button } from "../components/ui/Button";
import { NumberCard } from "../components/ui/NumberCard";
import { ProgressIndicator } from "../components/ui/ProgressIndicator";
import { useApp } from "../context/AppContext";
import { NUMBER_INSIGHTS } from "../types";

export function ProfileResultsScreen() {
  const { profile, setScreen, resetSession, updateDecision } = useApp();

  if (!profile) return null;

  const cards = [
    { key: "life_path_number" as const, value: profile.life_path_number },
    { key: "birthday_number" as const, value: profile.birthday_number },
    { key: "personal_year" as const, value: profile.personal_year },
    { key: "personal_month" as const, value: profile.personal_month },
  ];

  return (
    <div className="screen view-enter">
      <ProgressIndicator currentStep={1} />

      <header className="results-header">
        <p className="eyebrow">Reflective baseline</p>
        <h1 className="results-name">{profile.full_name}</h1>
        <p className="results-meta">
          Born {profile.date_of_birth}
          <span className="meta-sep" aria-hidden="true">
            ·
          </span>
          Focused on {profile.primary_goal}
        </p>
        <p className="results-lede">
          These numbers are a structured starting point for reflection — not a prediction
          of outcomes.
        </p>
      </header>

      <div className="number-grid" role="list">
        {cards.map((card, i) => {
          const insight = NUMBER_INSIGHTS[card.key];
          return (
            <NumberCard
              key={card.key}
              label={insight.label}
              value={card.value}
              blurb={insight.blurb}
              delay={0.07 * i}
            />
          );
        })}
      </div>

      <div className="goal-panel">
        <p className="goal-panel__label">Primary goal</p>
        <p className="goal-panel__value">{profile.primary_goal}</p>
        <p className="goal-panel__note">
          Your decision exploration will be oriented around this focus.
        </p>
      </div>

      <div className="form-actions">
        <Button
          onClick={() => {
            updateDecision({ decision_area: profile.primary_goal });
            setScreen("decision");
          }}
        >
          Frame your decision →
        </Button>
        <Button variant="ghost" onClick={resetSession}>
          Create another profile
        </Button>
      </div>
    </div>
  );
}
