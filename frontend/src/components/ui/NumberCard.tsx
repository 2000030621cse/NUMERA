type NumberCardProps = {
  label: string;
  value: number;
  blurb: string;
  delay?: number;
};

export function NumberCard({ label, value, blurb, delay = 0 }: NumberCardProps) {
  return (
    <article
      className="number-card"
      style={{ animationDelay: `${delay}s` }}
    >
      <p className="number-card__label">{label}</p>
      <p className="number-card__value">{value}</p>
      <p className="number-card__blurb">{blurb}</p>
    </article>
  );
}
