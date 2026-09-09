import type {
  DecisionAnalysis,
  DecisionContext,
  DecisionOption,
  NumerologyProfile,
} from "../types";

import { analysisToSnapshot, normalizeDecisionAnalysis } from "../types";



export function buildProfileSnapshot(profile: NumerologyProfile) {

  return {

    full_name: profile.full_name,

    date_of_birth: profile.date_of_birth,

    life_path_number: profile.life_path_number,

    birthday_number: profile.birthday_number,

    personal_year: profile.personal_year,

    personal_month: profile.personal_month,

    primary_goal: profile.primary_goal,

  };

}



export function buildDecisionPayload(decision: DecisionContext) {

  const user_options = (decision.user_options ?? [])
    .filter((o) => o.title.trim())
    .map((o) => ({ id: o.id, title: o.title.trim() }));



  return {

    decision_area: decision.decision_area,

    decision_question: decision.decision_question,

    why_considering: decision.why_considering,

    biggest_concern: decision.biggest_concern,

    priorities: decision.priorities,

    constraints: decision.constraints,

    risk_tolerance: decision.risk_tolerance,

    time_horizon: decision.time_horizon,

    context: decision.context,

    user_options,

  };

}



export function buildAnalyzePayload(

  profile: NumerologyProfile,

  decision: DecisionContext,

) {

  return {

    profile: buildProfileSnapshot(profile),

    decision: buildDecisionPayload(decision),

  };

}



export function buildFinalReportPayload(

  profile: NumerologyProfile,

  decision: DecisionContext,

  options: DecisionOption[],

  analysis: DecisionAnalysis,

) {

  const snapshot = analysisToSnapshot(normalizeDecisionAnalysis(analysis));



  return {

    profile: buildProfileSnapshot(profile),

    decision: buildDecisionPayload(decision),

    options,

    analysis: snapshot,

  };

}

