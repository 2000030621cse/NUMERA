import type {
  DecisionAnalysis,
  DecisionContext,
  DecisionInsightReport,
  DecisionOption,
  NumerologyProfile,
} from "../types";
import { normalizeDecisionInsightReport } from "../types";
import { buildFinalReportPayload } from "./sessionBuilder";

const ENDPOINT = "/api/numerology/decision-insight";

export async function fetchDecisionInsight(
  profile: NumerologyProfile,
  decision: DecisionContext,
  options: DecisionOption[],
  analysis: DecisionAnalysis,
): Promise<DecisionInsightReport> {
  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(
      buildFinalReportPayload(profile, decision, options, analysis),
    ),
  });

  if (!res.ok) {
    let message = "Unable to generate your decision report. Please try again.";
    try {
      const body = (await res.json()) as { detail?: unknown };
      if (typeof body.detail === "string") message = body.detail;
    } catch {
      // keep default
    }
    throw new Error(message);
  }

  const raw = (await res.json()) as Partial<DecisionInsightReport>;
  return normalizeDecisionInsightReport(raw, {
    decision_synthesis: analysis.decision_synthesis,
    key_tension: analysis.key_tension,
  });
}
