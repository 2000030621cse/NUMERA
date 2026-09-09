import type { DecisionAnalysis, DecisionContext, NumerologyProfile } from "../types";
import { normalizeDecisionAnalysis } from "../types";
import { buildAnalyzePayload } from "./sessionBuilder";

const ANALYZE_ENDPOINT = "/api/decision/analyze";

export type AnalyzeDecisionRequest = {
  profile: NumerologyProfile;
  decision: DecisionContext;
};

export async function analyzeDecision(
  request: AnalyzeDecisionRequest,
): Promise<DecisionAnalysis> {
  const res = await fetch(ANALYZE_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(buildAnalyzePayload(request.profile, request.decision)),
  });

  if (!res.ok) {
    let message = "Decision analysis failed. Please try again.";
    try {
      const body = (await res.json()) as { detail?: unknown };
      if (typeof body.detail === "string") message = body.detail;
    } catch {
      // keep default
    }
    throw new Error(message);
  }

  const raw = (await res.json()) as Partial<DecisionAnalysis>;
  return normalizeDecisionAnalysis(raw);
}
