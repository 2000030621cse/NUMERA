import { FormEvent, useState } from "react";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { ProgressIndicator } from "../components/ui/ProgressIndicator";
import { Select } from "../components/ui/Select";
import { SectionHeading } from "../components/ui/SectionHeading";
import { LoadingState } from "../components/ui/LoadingState";
import { ErrorState } from "../components/ui/ErrorState";
import { useApp } from "../context/AppContext";
import { createNumerologyProfile } from "../services/numerologyApi";
import { PRIMARY_GOALS, type PrimaryGoal } from "../types";

type FieldKey = "fullName" | "dateOfBirth" | "primaryGoal";

type ProfileScreenProps = {
  apiDown: boolean;
};

export function ProfileScreen({ apiDown }: ProfileScreenProps) {
  const { setProfile, setScreen } = useApp();
  const [fullName, setFullName] = useState("");
  const [dateOfBirth, setDateOfBirth] = useState("");
  const [primaryGoal, setPrimaryGoal] = useState<PrimaryGoal | "">("");
  const [fieldErrors, setFieldErrors] = useState<
    Partial<Record<FieldKey, string>>
  >({});
  const [formError, setFormError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  function validate(): Partial<Record<FieldKey, string>> {
    const errors: Partial<Record<FieldKey, string>> = {};
    if (!fullName.trim()) errors.fullName = "Full name is required.";
    if (!dateOfBirth) {
      errors.dateOfBirth = "Date of birth is required.";
    } else if (Number.isNaN(new Date(`${dateOfBirth}T00:00:00`).getTime())) {
      errors.dateOfBirth = "Enter a valid date of birth.";
    }
    if (!primaryGoal) errors.primaryGoal = "Select a primary goal.";
    return errors;
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setFormError(null);
    const errors = validate();
    setFieldErrors(errors);
    if (Object.keys(errors).length > 0) return;

    setIsSubmitting(true);
    try {
      const profile = await createNumerologyProfile({
        full_name: fullName.trim(),
        date_of_birth: dateOfBirth,
        primary_goal: primaryGoal as PrimaryGoal,
      });
      setProfile(profile);
      setScreen("profile-results");
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      setFormError(
        err instanceof Error ? err.message : "Something went wrong.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  if (isSubmitting) {
    return (
      <div className="screen view-enter">
        <LoadingState
          title="Building your profile…"
          message="Calculating your reflective numerology baseline."
        />
      </div>
    );
  }

  return (
    <div className="screen view-enter">
      <ProgressIndicator currentStep={1} />
      <SectionHeading
        eyebrow="NUMERA · Personal Decision Intelligence"
        title="Start with understanding yourself"
        subtitle="Your profile creates the reflective foundation for the decisions you explore."
      />

      <form className="panel-form panel-form--airy" onSubmit={handleSubmit} noValidate>
        <Input
          label="Full Name"
          name="full_name"
          autoComplete="name"
          placeholder="e.g. Priya Sharma"
          value={fullName}
          onChange={(e) => {
            setFullName(e.target.value);
            setFieldErrors((p) => ({ ...p, fullName: undefined }));
          }}
          hint="As you'd like it shown on your profile."
          error={fieldErrors.fullName}
        />

        <Input
          label="Date of Birth"
          name="date_of_birth"
          type="date"
          value={dateOfBirth}
          onChange={(e) => {
            setDateOfBirth(e.target.value);
            setFieldErrors((p) => ({ ...p, dateOfBirth: undefined }));
          }}
          hint="Used for Life Path, Birthday, and timing numbers — a reflective baseline."
          error={fieldErrors.dateOfBirth}
        />

        <Select
          label="Primary Goal"
          name="primary_goal"
          placeholder="Select where you want clarity"
          value={primaryGoal}
          onChange={(e) => {
            setPrimaryGoal(e.target.value as PrimaryGoal | "");
            setFieldErrors((p) => ({ ...p, primaryGoal: undefined }));
          }}
          options={PRIMARY_GOALS.map((g) => ({ value: g, label: g }))}
          hint="Frames how we'll prioritize decision exploration."
          error={fieldErrors.primaryGoal}
        />

        {formError ? <ErrorState message={formError} /> : null}

        <div className="form-actions">
          <Button type="submit" disabled={apiDown}>
            Create my profile →
          </Button>
          <Button variant="ghost" type="button" onClick={() => setScreen("landing")}>
            ← Back
          </Button>
        </div>

        <p className="form-trust-note">
          Your inputs drive Decision Compass. Numerology remains a reflective lens.
        </p>

        {apiDown ? (
          <p className="form-hint-banner" role="status">
            The NUMERA API is offline. Check that the backend is running, then try again.
          </p>
        ) : null}
      </form>
    </div>
  );
}
