import type {
  DecisionCompass,
  DecisionContext,
  DecisionOption,
  NumerologyProfile,
} from "../types";
import { normalizeDecisionCompass } from "../types";
import { buildAnalyzePayload } from "./sessionBuilder";

const ENDPOINT = "/api/decision/compass";

export async function fetchDecisionCompass(
  profile: NumerologyProfile,
  decision: DecisionContext,
  options: DecisionOption[],
): Promise<DecisionCompass> {
  const base = buildAnalyzePayload(profile, decision);
  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ...base, options }),
  });

  if (!res.ok) {
    throw new Error("Unable to compute Decision Compass.");
  }

  const raw = (await res.json()) as Partial<DecisionCompass>;
  const compass = normalizeDecisionCompass(raw);
  if (!compass) throw new Error("Invalid Decision Compass response.");
  return compass;
}
