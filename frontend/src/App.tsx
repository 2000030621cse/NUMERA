import { useEffect } from "react";
import { AppProvider, useApp } from "./context/AppContext";
import { useApiHealth } from "./hooks/useApiHealth";
import { Header } from "./components/layout/Header";
import { Footer } from "./components/layout/Footer";
import { LandingScreen } from "./screens/LandingScreen";
import { ProfileScreen } from "./screens/ProfileScreen";
import { ProfileResultsScreen } from "./screens/ProfileResultsScreen";
import { DecisionExplorationScreen } from "./screens/DecisionExplorationScreen";
import { DecisionIntelligenceScreen } from "./screens/DecisionIntelligenceScreen";
import { WhatIfScreen } from "./screens/WhatIfScreen";
import { FinalReportScreen } from "./screens/FinalReportScreen";
import { LoadingState } from "./components/ui/LoadingState";
import "./App.css";

function AppShell() {
  const apiHealth = useApiHealth();
  const { screen, profile, analysis, scenarios, goToLanding, setScreen } =
    useApp();

  useEffect(() => {
    if (screen === "profile-results" && !profile) setScreen("landing");
    else if (screen === "decision" && !profile) setScreen("landing");
    else if (screen === "intelligence" && !profile) setScreen("landing");
    else if (screen === "intelligence" && profile && !analysis) {
      setScreen("decision");
    } else if (screen === "what-if" && scenarios.length === 0) {
      setScreen(analysis ? "intelligence" : "landing");
    } else if (screen === "final-report" && !profile) {
      setScreen("landing");
    } else if (screen === "final-report" && profile && !analysis) {
      setScreen("decision");
    } else if (screen === "final-report" && profile && analysis && scenarios.length === 0) {
      setScreen("intelligence");
    }
  }, [screen, profile, analysis, scenarios.length, setScreen]);

  function renderScreen() {
    switch (screen) {
      case "landing":
        return <LandingScreen />;
      case "profile":
        return <ProfileScreen apiDown={apiHealth === "down"} />;
      case "profile-results":
        return <ProfileResultsScreen />;
      case "decision":
        return <DecisionExplorationScreen />;
      case "intelligence":
        if (!analysis) {
          return (
            <LoadingState
              title="Loading your analysis"
              message="Preparing your decision intelligence…"
            />
          );
        }
        return <DecisionIntelligenceScreen />;
      case "what-if":
        return <WhatIfScreen />;
      case "final-report":
        if (!profile || !analysis) {
          return (
            <LoadingState
              title="Preparing your report"
              message="Loading your decision session…"
            />
          );
        }
        return <FinalReportScreen />;
      default:
        return <LandingScreen />;
    }
  }

  return (
    <div className="page">
      <div className="atmosphere" aria-hidden="true" />
      <Header apiHealth={apiHealth} onLogoClick={goToLanding} />
      <main id="top" className="main">
        {renderScreen()}
      </main>
      <Footer />
    </div>
  );
}

export default function App() {
  return (
    <AppProvider>
      <AppShell />
    </AppProvider>
  );
}
