import { Button } from "../components/ui/Button";
import { useApp } from "../context/AppContext";
import { HOW_IT_WORKS, PRODUCT_PILLARS } from "../types";

export function LandingScreen() {
  const { setScreen } = useApp();

  function scrollToHowItWorks() {
    document.getElementById("how-it-works")?.scrollIntoView({ behavior: "smooth" });
  }

  return (
    <div className="screen screen--landing view-enter">
      <section className="hero hero--gate" aria-labelledby="hero-brand">
        <p className="hero-kicker">Personal Decision Intelligence</p>
        <h1 id="hero-brand" className="hero-brand">
          NUMERA
        </h1>
        <p className="hero-lede">Make complex decisions with more clarity.</p>
        <p className="hero-body">
          Numerology is a reflective lens. Decision Compass compares your options against
          what you said matters. AI synthesizes — it does not predict your future.
        </p>
        <div className="hero-actions">
          <Button onClick={() => setScreen("profile")}>Begin →</Button>
          <Button variant="ghost" onClick={scrollToHowItWorks}>
            How NUMERA works
          </Button>
        </div>
      </section>

      <div className="divider" aria-hidden="true" />

      <section className="pillars" aria-label="Product pillars">
        {PRODUCT_PILLARS.map((pillar) => (
          <article key={pillar.title} className="pillar">
            <h2 className="pillar-title">{pillar.title}</h2>
            <p className="pillar-body">{pillar.body}</p>
          </article>
        ))}
      </section>

      <section
        id="how-it-works"
        className="how-it-works"
        aria-labelledby="how-heading"
      >
        <h2 id="how-heading" className="how-it-works__title">
          How it works
        </h2>
        <ol className="how-it-works__list">
          {HOW_IT_WORKS.map((item) => (
            <li key={item.step} className="how-step">
              <span className="how-step__num">{item.step}</span>
              <span className="how-step__title">{item.title}</span>
            </li>
          ))}
        </ol>
      </section>
    </div>
  );
}
