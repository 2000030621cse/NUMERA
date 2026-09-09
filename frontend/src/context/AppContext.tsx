import {

  createContext,

  useCallback,

  useContext,

  useEffect,

  useMemo,

  useState,

  type ReactNode,

} from "react";

import {
  EMPTY_DECISION,
  decisionInputKey,
  normalizeDecisionAnalysis,
  normalizeDecisionContext,
  normalizeDecisionInsightReport,
  optionToScenario,
  type DecisionAnalysis,
  type DecisionContext,
  type DecisionInsightReport,
  type NumerologyProfile,
  type Screen,
  type WhatIfScenario,
} from "../types";



const SESSION_KEY = "numera-session";



type SessionSnapshot = {

  screen: Screen;

  profile: NumerologyProfile | null;

  decision: DecisionContext;

  analysis: DecisionAnalysis | null;

  analysisInputKey: string | null;

  scenarios: WhatIfScenario[];

  finalReport: DecisionInsightReport | null;

};



type AppContextValue = {

  screen: Screen;

  profile: NumerologyProfile | null;

  decision: DecisionContext;

  analysis: DecisionAnalysis | null;

  scenarios: WhatIfScenario[];

  finalReport: DecisionInsightReport | null;

  setScreen: (screen: Screen) => void;

  setProfile: (profile: NumerologyProfile | null) => void;

  setDecision: (decision: DecisionContext) => void;

  updateDecision: (partial: Partial<DecisionContext>) => void;

  setAnalysis: (analysis: DecisionAnalysis | null) => void;

  setScenarios: (scenarios: WhatIfScenario[]) => void;

  setFinalReport: (report: DecisionInsightReport | null) => void;

  resetSession: () => void;

  goToLanding: () => void;

  invalidateDownstream: () => void;
  commitAnalysisResult: (analysis: DecisionAnalysis) => void;
};



const AppContext = createContext<AppContextValue | null>(null);



function loadSession(): Partial<SessionSnapshot> | null {

  try {

    const raw = sessionStorage.getItem(SESSION_KEY);

    if (!raw) return null;

    const parsed = JSON.parse(raw) as Partial<SessionSnapshot>;

    if (parsed.decision) {
      parsed.decision = normalizeDecisionContext(parsed.decision);
    }

    if (parsed.analysis) {
      parsed.analysis = normalizeDecisionAnalysis(parsed.analysis);
    }

    if (parsed.finalReport) {
      parsed.finalReport = normalizeDecisionInsightReport(parsed.finalReport);
    }

    return parsed;

  } catch {

    return null;

  }

}



function saveSession(snapshot: SessionSnapshot) {

  try {

    sessionStorage.setItem(SESSION_KEY, JSON.stringify(snapshot));

  } catch {

    // storage unavailable — continue without persistence

  }

}



export function AppProvider({ children }: { children: ReactNode }) {

  const saved = loadSession();



  const [screen, setScreen] = useState<Screen>(saved?.screen ?? "landing");

  const [profile, setProfileState] = useState<NumerologyProfile | null>(

    saved?.profile ?? null,

  );

  const [decision, setDecisionState] = useState<DecisionContext>(

    saved?.decision ?? EMPTY_DECISION,

  );

  const [analysis, setAnalysisState] = useState<DecisionAnalysis | null>(

    saved?.analysis ? normalizeDecisionAnalysis(saved.analysis) : null,

  );

  const [analysisInputKey, setAnalysisInputKey] = useState<string | null>(

    saved?.analysisInputKey ?? null,

  );

  const [scenarios, setScenarios] = useState<WhatIfScenario[]>(

    saved?.scenarios ?? [],

  );

  const [finalReport, setFinalReport] = useState<DecisionInsightReport | null>(

    saved?.finalReport ?? null,

  );



  const invalidateDownstream = useCallback(() => {

    setAnalysisState(null);

    setAnalysisInputKey(null);

    setScenarios([]);

    setFinalReport(null);

  }, []);



  const setProfile = useCallback(

    (next: NumerologyProfile | null) => {

      setProfileState(next);

      invalidateDownstream();

    },

    [invalidateDownstream],

  );



  const applyDecisionUpdate = useCallback(

    (updater: (prev: DecisionContext) => DecisionContext) => {

      setDecisionState((prev) => {

        const next = updater(prev);

        const prevKey = analysisInputKey ?? decisionInputKey(prev);

        const nextKey = decisionInputKey(next);

        if (analysis && prevKey !== nextKey) {

          setAnalysisState(null);

          setAnalysisInputKey(null);

          setScenarios([]);

          setFinalReport(null);

        }

        return next;

      });

    },

    [analysis, analysisInputKey],

  );



  const setDecision = useCallback(

    (next: DecisionContext) => {

      applyDecisionUpdate(() => next);

    },

    [applyDecisionUpdate],

  );



  const updateDecision = useCallback(

    (partial: Partial<DecisionContext>) => {

      applyDecisionUpdate((prev) => ({ ...prev, ...partial }));

    },

    [applyDecisionUpdate],

  );



  const setAnalysisWithKey = useCallback(

    (next: DecisionAnalysis | null) => {

      if (next) {
        const normalized = normalizeDecisionAnalysis(next);
        setAnalysisState(normalized);
        setAnalysisInputKey(decisionInputKey(decision));
      } else {
        setAnalysisState(null);
        setAnalysisInputKey(null);
      }

    },

    [decision],

  );



  const commitAnalysisResult = useCallback(

    (result: DecisionAnalysis) => {

      const normalized = normalizeDecisionAnalysis(result);

      setAnalysisState(normalized);

      setAnalysisInputKey(decisionInputKey(decision));

      setScenarios(normalized.options.map(optionToScenario));

      setFinalReport(null);

      setScreen("intelligence");

    },

    [decision],

  );



  const setScenariosWithInvalidation = useCallback((next: WhatIfScenario[]) => {

    setScenarios(next);

    setFinalReport(null);

  }, []);



  useEffect(() => {

    saveSession({

      screen,

      profile,

      decision,

      analysis,

      analysisInputKey,

      scenarios,

      finalReport,

    });

  }, [

    screen,

    profile,

    decision,

    analysis,

    analysisInputKey,

    scenarios,

    finalReport,

  ]);



  const resetSession = useCallback(() => {

    setProfileState(null);

    setDecisionState(EMPTY_DECISION);

    setAnalysisState(null);

    setAnalysisInputKey(null);

    setScenarios([]);

    setFinalReport(null);

    setScreen("landing");

    sessionStorage.removeItem(SESSION_KEY);

  }, []);



  const goToLanding = useCallback(() => {

    setScreen("landing");

    window.scrollTo({ top: 0, behavior: "smooth" });

  }, []);



  const value = useMemo(

    () => ({

      screen,

      profile,

      decision,

      analysis,

      scenarios,

      finalReport,

      setScreen,

      setProfile,

      setDecision,

      updateDecision,

      setAnalysis: setAnalysisWithKey,

      setScenarios: setScenariosWithInvalidation,

      setFinalReport,

      resetSession,

      goToLanding,

      commitAnalysisResult,

      invalidateDownstream,

    }),

    [

      screen,

      profile,

      decision,

      analysis,

      scenarios,

      finalReport,

      updateDecision,

      setAnalysisWithKey,

      setScenariosWithInvalidation,

      resetSession,

      goToLanding,

      commitAnalysisResult,

      invalidateDownstream,

    ],

  );



  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;

}



export function useApp() {

  const ctx = useContext(AppContext);

  if (!ctx) throw new Error("useApp must be used within AppProvider");

  return ctx;

}

