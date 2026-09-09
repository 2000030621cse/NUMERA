type LoadingStateProps = {
  title: string;
  message: string;
};

export function LoadingState({ title, message }: LoadingStateProps) {
  return (
    <div className="loading-state" role="status" aria-live="polite">
      <div className="loading-state__pulse" aria-hidden="true" />
      <p className="loading-state__title">{title}</p>
      <p className="loading-state__message">{message}</p>
    </div>
  );
}
