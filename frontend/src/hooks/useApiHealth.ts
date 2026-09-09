import { useEffect, useState } from "react";
import type { HealthState } from "../types";

export function useApiHealth(pollMs = 5000): HealthState {
  const [state, setState] = useState<HealthState>("checking");

  useEffect(() => {
    let cancelled = false;

    async function check() {
      try {
        const res = await fetch("/health");
        if (!cancelled) setState(res.ok ? "ok" : "down");
      } catch {
        if (!cancelled) setState("down");
      }
    }

    void check();
    const id = window.setInterval(() => void check(), pollMs);
    return () => {
      cancelled = true;
      window.clearInterval(id);
    };
  }, [pollMs]);

  return state;
}
