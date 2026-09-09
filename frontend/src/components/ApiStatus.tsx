import type { HealthState } from "../types";

type ApiStatusProps = {
  state: HealthState;
};

export function ApiStatus({ state }: ApiStatusProps) {
  const label =
    state === "checking" ? "Checking" : state === "ok" ? "Online" : "Offline";

  return (
    <div
      className={`api-status api-status--${state}`}
      role="status"
      aria-live="polite"
      title={`NUMERA API ${label.toLowerCase()}`}
    >
      <span className="api-status__dot" aria-hidden="true" />
      <span className="api-status__text">API {label}</span>
    </div>
  );
}
