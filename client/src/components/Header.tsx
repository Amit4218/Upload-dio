import { useTheme } from "@/hooks/Theme";
import { Moon, Sun } from "lucide-react";
import { FaGithub } from "react-icons/fa6";
import { Button } from "@/components/ui/button";
import { NavLink } from "react-router-dom";

export default function Header() {
  const { resolvedTheme, toggleTheme } = useTheme();

  return (
    <div className="flex justify-between px-4 md:px-10 py-2">
      <NavLink to="/">
        <img src="/logo.png" alt="uplodio logo" className="h-7 w-auto" />
      </NavLink>

      <div className="flex items-center gap-1">
        <Button
          className={"border-0 bg-0 -px-0.5"}
          size={"icon-lg"}
          variant={"link"}
          onClick={toggleTheme}
        >
          {resolvedTheme === "dark" ? <Sun /> : <Moon />}
        </Button>

        <NavLink
          to="https://github.com/amit4218/upload-dio"
          target="_blank"
          rel="noopener noreferrer"
        >
          <FaGithub size={20} />
        </NavLink>
      </div>
    </div>
  );
}
