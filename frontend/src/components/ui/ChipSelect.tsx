type ChipSelectProps = {
  label: string;
  options: readonly string[];
  selected: string[];
  onChange: (selected: string[]) => void;
  hint?: string;
  error?: string;
};

export function ChipSelect({
  label,
  options,
  selected,
  onChange,
  hint,
  error,
}: ChipSelectProps) {
  function toggle(option: string) {
    if (selected.includes(option)) {
      onChange(selected.filter((s) => s !== option));
    } else {
      onChange([...selected, option]);
    }
  }

  return (
    <fieldset className="chip-fieldset">
      <legend className="field-label">{label}</legend>
      <div className="chip-grid" role="group" aria-label={label}>
        {options.map((option) => {
          const isSelected = selected.includes(option);
          return (
            <button
              key={option}
              type="button"
              className={`chip${isSelected ? " chip--selected" : ""}`}
              aria-pressed={isSelected}
              onClick={() => toggle(option)}
            >
              {option}
            </button>
          );
        })}
      </div>
      {error ? (
        <span className="field-error" role="alert">
          {error}
        </span>
      ) : hint ? (
        <span className="field-hint">{hint}</span>
      ) : null}
    </fieldset>
  );
}
