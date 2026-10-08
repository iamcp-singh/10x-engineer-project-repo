export default function ErrorMessage({ message, onDismiss }) {
  return (
    <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded relative" role="alert">
      <span className="block sm:inline">{message}</span>
      {onDismiss && (
        <button
          onClick={onDismiss}
          className="absolute top-0 bottom-0 right-0 px-4 py-3 hover:text-red-900"
          aria-label="Dismiss"
        >
          <span className="text-xl">&times;</span>
        </button>
      )}
    </div>
  );
}
