import { LoaderCircle } from "lucide-react";

export default function Loader() {
  return (
    <div className="flex h-screen items-center justify-center bg-background">
      <LoaderCircle className="h-10 w-10 animate-spin text-primary" />
    </div>
  );
}
