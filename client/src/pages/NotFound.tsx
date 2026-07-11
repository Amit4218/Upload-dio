import { Link } from "react-router-dom";

function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4">
      <h1 className="text-5xl font-bold">404</h1>

      <p className="text-muted-foreground">
        The page you're looking for doesn't exist.
      </p>

      <Link
        to="/dashboard"
        className="rounded-md bg-primary px-4 py-2 text-primary-foreground"
      >
        Go to Dashboard
      </Link>
    </div>
  );
}

export default NotFound;
