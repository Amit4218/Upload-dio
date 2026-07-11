import { LoaderCircle } from "lucide-react";

export default function Loader() {
  return (
    <div className="flex items-center justify-center bg-background mt-60">
      <LoaderCircle className="h-10 w-10 animate-spin text-primary" />
    </div>
  );
}
