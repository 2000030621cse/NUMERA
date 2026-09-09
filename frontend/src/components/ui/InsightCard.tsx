type InsightCardProps = {
  type: string;
  title: string;
  body: string;
  delay?: number;
};

export function InsightCard({ type, title, body, delay = 0 }: InsightCardProps) {
  return (
    <article
      className="insight-card"
      style={{ animationDelay: `${delay}s` }}
    >
      <p className="insight-card__type">{type}</p>
      <h3 className="insight-card__title">{title}</h3>
      <p className="insight-card__body">{body}</p>
    </article>
  );
}
