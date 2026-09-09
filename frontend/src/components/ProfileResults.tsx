import { NUMBER_INSIGHTS, type NumerologyProfile } from "../types";

type ProfileResultsProps = {
  profile: NumerologyProfile;
  onReset: () => void;
  onExplore: () => void;
};

export function ProfileResults({
  profile,
  onReset,
  onExplore,
}: ProfileResultsProps) {
  const cards = [
    {
      key: "life_path_number" as const,
      value: profile.life_path_number,
    },
    {
      key: "birthday_number" as const,
      value: profile.birthday_number,
    },
    {
      key: "personal_year" as const,
      value: profile.personal_year,
    },
    {
      key: "personal_month" as const,
      value: profile.personal_month,
    },
  ];

  return (
    <section className="results" aria-labelledby="results-heading">
      <div className="results-header">
        <p className="eyebrow">Personal Numerology Profile</p>
        <h2 id="results-heading" className="results-name">
          {profile.full_name}
        </h2>
        <p className="results-meta">
          Born {profile.date_of_birth}
          <span className="meta-sep" aria-hidden="true">
            ·
          </span>
          Focused on {profile.primary_goal}
        </p>
      </div>

      <div className="number-grid" role="list">
        {cards.map((card, index) => {
          const insight = NUMBER_INSIGHTS[card.key];
          return (
            <article
              key={card.key}
              className="number-card"
              role="listitem"
              style={{ animationDelay: `${0.08 * index}s` }}
            >
              <p className="number-card__label">{insight.label}</p>
              <p className="number-card__value">{card.value}</p>
              <p className="number-card__blurb">{insight.blurb}</p>
            </article>
          );
        })}
      </div>

      <div className="goal-panel">
        <p className="goal-panel__label">Primary goal</p>
        <p className="goal-panel__value">{profile.primary_goal}</p>
        <p className="goal-panel__note">
          Upcoming decision exploration will be oriented around this focus.
        </p>
      </div>

      <div className="results-actions">
        <button type="button" className="btn-primary" onClick={onExplore}>
          Explore a decision →
        </button>
        <button type="button" className="btn-ghost" onClick={onReset}>
          Create another profile
        </button>
      </div>

      <p className="results-footnote" role="note">
        Decision exploration arrives in a later phase. Your numbers are ready
        whenever you are.
      </p>
    </section>
  );
}
