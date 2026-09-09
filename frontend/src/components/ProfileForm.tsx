import { FormEvent } from "react";
import { PRIMARY_GOALS, type PrimaryGoal } from "../types";

type ProfileFormProps = {
  fullName: string;
  dateOfBirth: string;
  primaryGoal: PrimaryGoal | "";
  formError: string | null;
  fieldErrors: Partial<Record<"fullName" | "dateOfBirth" | "primaryGoal", string>>;
  isSubmitting: boolean;
  apiDown: boolean;
  onFullNameChange: (value: string) => void;
  onDateOfBirthChange: (value: string) => void;
  onPrimaryGoalChange: (value: PrimaryGoal | "") => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
};

export function ProfileForm({
  fullName,
  dateOfBirth,
  primaryGoal,
  formError,
  fieldErrors,
  isSubmitting,
  apiDown,
  onFullNameChange,
  onDateOfBirthChange,
  onPrimaryGoalChange,
  onSubmit,
}: ProfileFormProps) {
  return (
    <form
      className="profile-form"
      onSubmit={onSubmit}
      noValidate
      aria-describedby={formError ? "form-error" : undefined}
    >
      <div className="form-intro">
        <h2 className="form-title">Create your personal profile</h2>
        <p className="form-lede">
          Enter your details to generate a deterministic numerology baseline —
          no AI interpretation yet, only clear numbers you can trust.
        </p>
      </div>

      <label className="field">
        <span className="field-label">Full Name</span>
        <input
          type="text"
          name="full_name"
          autoComplete="name"
          placeholder="e.g. Priya Sharma"
          value={fullName}
          onChange={(e) => onFullNameChange(e.target.value)}
          disabled={isSubmitting}
          aria-invalid={Boolean(fieldErrors.fullName)}
          aria-describedby={fieldErrors.fullName ? "err-full-name" : undefined}
        />
        {fieldErrors.fullName ? (
          <span id="err-full-name" className="field-error">
            {fieldErrors.fullName}
          </span>
        ) : (
          <span className="field-hint">As you’d like it shown on your profile.</span>
        )}
      </label>

      <label className="field">
        <span className="field-label">Date of Birth</span>
        <input
          type="date"
          name="date_of_birth"
          value={dateOfBirth}
          onChange={(e) => onDateOfBirthChange(e.target.value)}
          disabled={isSubmitting}
          aria-invalid={Boolean(fieldErrors.dateOfBirth)}
          aria-describedby={
            fieldErrors.dateOfBirth ? "err-dob" : "hint-dob"
          }
        />
        {fieldErrors.dateOfBirth ? (
          <span id="err-dob" className="field-error">
            {fieldErrors.dateOfBirth}
          </span>
        ) : (
          <span id="hint-dob" className="field-hint">
            Used for Life Path, Birthday, and timing numbers.
          </span>
        )}
      </label>

      <label className="field">
        <span className="field-label">Primary Goal</span>
        <select
          name="primary_goal"
          value={primaryGoal}
          onChange={(e) =>
            onPrimaryGoalChange(e.target.value as PrimaryGoal | "")
          }
          disabled={isSubmitting}
          aria-invalid={Boolean(fieldErrors.primaryGoal)}
          aria-describedby={
            fieldErrors.primaryGoal ? "err-goal" : "hint-goal"
          }
        >
          <option value="">Select where you want clarity</option>
          {PRIMARY_GOALS.map((goal) => (
            <option key={goal} value={goal}>
              {goal}
            </option>
          ))}
        </select>
        {fieldErrors.primaryGoal ? (
          <span id="err-goal" className="field-error">
            {fieldErrors.primaryGoal}
          </span>
        ) : (
          <span id="hint-goal" className="field-hint">
            Frames how we’ll prioritize upcoming decision guidance.
          </span>
        )}
      </label>

      {formError ? (
        <p id="form-error" className="form-error" role="alert">
          {formError}
        </p>
      ) : null}

      <button
        type="submit"
        className="btn-primary"
        disabled={isSubmitting || apiDown}
      >
        {isSubmitting ? "Creating your profile…" : "Create My Profile"}
      </button>

      {apiDown ? (
        <p className="form-hint-banner" role="status">
          The NUMERA API is offline. Check that the backend is running, then try again.
        </p>
      ) : null}
    </form>
  );
}
