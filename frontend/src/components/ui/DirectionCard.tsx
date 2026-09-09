import type { PossibleDirection } from "../../types";
import { toStringList } from "../../types";

type DirectionCardProps = {
  direction: PossibleDirection;
  delay?: number;
};

export function DirectionCard({ direction, delay = 0 }: DirectionCardProps) {
  const questions = toStringList(direction.questions);

  return (
    <article
      className="direction-card"
      style={{ animationDelay: `${delay}s` }}
    >
      <p className="direction-card__label">{direction.label}</p>
      <h3 className="direction-card__title">{direction.title}</h3>
      <div className="direction-card__block">
        <p className="direction-card__heading">Potential upside</p>
        <p>{direction.upside}</p>
      </div>
      <div className="direction-card__block">
        <p className="direction-card__heading">Potential trade-off</p>
        <p>{direction.tradeoff}</p>
      </div>
      <div className="direction-card__block">
        <p className="direction-card__heading">Questions to consider</p>
        <ul>
          {questions.map((q) => (
            <li key={q}>{q}</li>
          ))}
        </ul>
      </div>
    </article>
  );
}
