import { JOURNEY_STEPS, type JourneyStep } from "../../types";

type ProgressIndicatorProps = {
  currentStep: JourneyStep;
};

export function ProgressIndicator({ currentStep }: ProgressIndicatorProps) {
  const current = JOURNEY_STEPS.find((s) => s.id === currentStep);
  const total = JOURNEY_STEPS.length;

  return (
    <nav className="progress" aria-label="Product journey progress">
      <p className="progress__condensed">
        {String(currentStep).padStart(2, "0")} / {String(total).padStart(2, "0")}
        {current ? ` · ${current.label}` : ""}
      </p>
      <ol className="progress__list">
        {JOURNEY_STEPS.map((step, index) => {
          const isActive = step.id === currentStep;
          const isComplete = step.id < currentStep;
          return (
            <li
              key={step.id}
              className={`progress__item${isActive ? " progress__item--active" : ""}${isComplete ? " progress__item--complete" : ""}`}
              aria-current={isActive ? "step" : undefined}
            >
              {index > 0 ? <span className="progress__connector" aria-hidden="true" /> : null}
              <span className="progress__dot" aria-hidden="true" />
              <span className="progress__num">
                {String(step.id).padStart(2, "0")}
              </span>
              <span className="progress__label">{step.label}</span>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
