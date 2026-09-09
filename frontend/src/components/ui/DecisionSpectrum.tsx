import { useCountUp } from "../../hooks/useCountUp";
import type { DecisionCompass, OptionCompassScore } from "../../types";

type DecisionSpectrumProps = {
  compass: DecisionCompass;
  /** Compact mode for embedding inside report chapters */
  compact?: boolean;
};

/** Minimum horizontal gap (%) between markers so labels/dots don't collide. */
const MIN_MARK_GAP = 16;

type LaidOutMark = {
  score: OptionCompassScore;
  left: number;
};

/**
 * Place markers by alignment score, then nudge apart when scores are
 * identical or very close. Does not change the underlying scores.
 */
function layoutMarkPositions(scores: OptionCompassScore[]): LaidOutMark[] {
  const items = scores.map((score) => ({
    score,
    left: Math.min(92, Math.max(8, score.numera_alignment)),
  }));

  items.sort((a, b) => a.left - b.left || a.score.option_title.localeCompare(b.score.option_title));

  for (let i = 1; i < items.length; i++) {
    const prev = items[i - 1];
    const cur = items[i];
    if (cur.left - prev.left < MIN_MARK_GAP) {
      cur.left = Math.min(92, prev.left + MIN_MARK_GAP);
    }
  }

  // If nudging pushed past the right edge, pull the cluster left
  const overflow = items[items.length - 1]?.left ?? 0;
  if (overflow > 92) {
    const shift = overflow - 92;
    for (const item of items) {
      item.left = Math.max(8, item.left - shift);
    }
  }

  // Re-check left collisions after pull
  for (let i = 1; i < items.length; i++) {
    if (items[i].left - items[i - 1].left < MIN_MARK_GAP) {
      items[i].left = Math.min(92, items[i - 1].left + MIN_MARK_GAP);
    }
  }

  return items;
}

function ScoreMark({
  score,
  left,
  isLeader,
  showLeaderLabel,
  animate,
  stackIndex,
}: {
  score: OptionCompassScore;
  left: number;
  isLeader: boolean;
  showLeaderLabel: boolean;
  animate: boolean;
  stackIndex: number;
}) {
  const display = useCountUp(Math.round(score.numera_alignment), 600, animate);
  // Preserve one decimal when present in source score
  const hasDecimal = !Number.isInteger(score.numera_alignment);
  const label = hasDecimal
    ? score.numera_alignment.toFixed(1)
    : String(display);

  return (
    <div
      className={`spectrum-mark${isLeader ? " spectrum-mark--leader" : ""}`}
      style={{
        left: `${left}%`,
        zIndex: 10 + stackIndex,
      }}
      title={`${score.option_title}: ${score.numera_alignment}/100`}
    >
      {showLeaderLabel && isLeader ? (
        <span className="spectrum-mark__badge">Currently strongest</span>
      ) : null}
      <span className="spectrum-mark__dot" aria-hidden="true" />
      <span className="spectrum-mark__score">
        <span className="spectrum-mark__score-num">{label}</span>
        <span className="spectrum-mark__score-den">/100</span>
      </span>
    </div>
  );
}

function VerticalBar({
  score,
  isLeader,
  rank,
  animate,
}: {
  score: OptionCompassScore;
  isLeader: boolean;
  rank: number;
  animate: boolean;
}) {
  const display = useCountUp(Math.round(score.numera_alignment), 600, animate);
  const width = Math.min(100, Math.max(4, score.numera_alignment));
  const hasDecimal = !Number.isInteger(score.numera_alignment);
  const label = hasDecimal ? score.numera_alignment.toFixed(1) : String(display);

  return (
    <li
      className={`spectrum-bar${isLeader ? " spectrum-bar--leader" : ""}`}
      style={{ animationDelay: `${rank * 70}ms` }}
    >
      <div className="spectrum-bar__meta">
        <span className="spectrum-bar__title">{score.option_title}</span>
        <span
          className="spectrum-bar__score"
          aria-label={`${score.numera_alignment} out of 100`}
        >
          {label}
          <span className="spectrum-bar__den">/100</span>
        </span>
      </div>
      <div
        className="spectrum-bar__track"
        role="img"
        aria-label={`Alignment ${score.numera_alignment} of 100`}
      >
        <div className="spectrum-bar__fill" style={{ width: `${width}%` }} />
      </div>
      {isLeader ? (
        <p className="spectrum-bar__leader-label">Currently strongest alignment</p>
      ) : null}
    </li>
  );
}

export function DecisionSpectrum({ compass, compact = false }: DecisionSpectrumProps) {
  const { scores, strongest } = compass;
  const sorted = [...scores].sort((a, b) => b.numera_alignment - a.numera_alignment);
  const hasLeader = strongest.has_clear_leader;
  const leaderId = hasLeader ? strongest.option_id : "";
  const laidOut = layoutMarkPositions(scores);

  return (
    <div className={`spectrum${compact ? " spectrum--compact" : ""}`}>
      <div className="spectrum__status" role="status">
        {hasLeader ? (
          <>
            <p className="spectrum__status-label">Currently strongest alignment</p>
            <p className="spectrum__status-title">{strongest.title}</p>
          </>
        ) : (
          <>
            <p className="spectrum__status-label">Alignment status</p>
            <p className="spectrum__status-title">No clear leader yet</p>
            {strongest.no_leader_reason || strongest.reason ? (
              <p className="spectrum__status-reason">
                {strongest.no_leader_reason || strongest.reason}
              </p>
            ) : null}
          </>
        )}
      </div>

      {/* Desktop / tablet horizontal spectrum */}
      <div
        className="spectrum-track-wrap"
        role="img"
        aria-label="Decision spectrum showing NUMERA Alignment for each option"
      >
        <div className="spectrum-track" aria-hidden="true">
          <span className="spectrum-track__end spectrum-track__end--low">Lower</span>
          <span className="spectrum-track__end spectrum-track__end--high">Higher</span>
        </div>
        <div className="spectrum-marks">
          {laidOut.map((item, i) => (
            <ScoreMark
              key={item.score.option_id}
              score={item.score}
              left={item.left}
              isLeader={hasLeader && item.score.option_id === leaderId}
              showLeaderLabel={hasLeader}
              animate
              stackIndex={i}
            />
          ))}
        </div>
      </div>

      {/* Option legend — always below the track so titles never collide */}
      <ol className="spectrum-legend spectrum-legend--desktop" aria-label="Options on the spectrum">
        {sorted.map((score) => {
          const isLeader = hasLeader && score.option_id === leaderId;
          const value = Number.isInteger(score.numera_alignment)
            ? String(score.numera_alignment)
            : score.numera_alignment.toFixed(1);
          return (
            <li
              key={score.option_id}
              className={`spectrum-legend__item${isLeader ? " spectrum-legend__item--leader" : ""}`}
            >
              <span className="spectrum-legend__dot" aria-hidden="true" />
              <span className="spectrum-legend__title">{score.option_title}</span>
              <span className="spectrum-legend__score">
                {value}
                <span className="spectrum-legend__den">/100</span>
              </span>
            </li>
          );
        })}
      </ol>

      <p className="spectrum-track__caption">
        Position reflects alignment with what you told NUMERA — not a predicted outcome.
        Markers may be spaced slightly for readability when scores are close.
      </p>

      {/* Mobile vertical bars */}
      <ol className="spectrum-bars" aria-label="NUMERA Alignment by option">
        {sorted.map((score, i) => (
          <VerticalBar
            key={score.option_id}
            score={score}
            isLeader={hasLeader && score.option_id === leaderId}
            rank={i}
            animate
          />
        ))}
      </ol>
    </div>
  );
}
