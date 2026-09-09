import type { NumerologyProfile, PrimaryGoal } from "../types";

export type CreateProfilePayload = {
  full_name: string;
  date_of_birth: string;
  primary_goal: PrimaryGoal;
};

export async function createNumerologyProfile(
  payload: CreateProfilePayload,
): Promise<NumerologyProfile> {
  const res = await fetch("/api/numerology/profile", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      full_name: payload.full_name,
      date_of_birth: payload.date_of_birth,
    }),
  });

  if (!res.ok) {
    let message = "Unable to create your profile. Please try again.";
    try {
      const body = (await res.json()) as { detail?: unknown };
      if (typeof body.detail === "string") {
        message = body.detail;
      } else if (Array.isArray(body.detail) && body.detail.length > 0) {
        const first = body.detail[0] as { msg?: string };
        message = first.msg ?? message;
      }
    } catch {
      // keep default
    }
    throw new Error(message);
  }

  const data = (await res.json()) as Omit<NumerologyProfile, "primary_goal">;
  return { ...data, primary_goal: payload.primary_goal };
}
