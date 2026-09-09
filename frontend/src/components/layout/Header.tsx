import { ApiStatus } from "../ApiStatus";
import type { HealthState } from "../../types";

type HeaderProps = {
  apiHealth: HealthState;
  onLogoClick?: () => void;
};

export function Header({ apiHealth, onLogoClick }: HeaderProps) {
  return (
    <header className="topbar">
      <button type="button" className="logo" onClick={onLogoClick}>
        NUMERA
      </button>
      <ApiStatus state={apiHealth} />
    </header>
  );
}
