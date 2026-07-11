import { useTheme } from "@/hooks/Theme";
import { Moon, Sun } from "lucide-react";
import { FaGithub } from "react-icons/fa6";
import { Button } from "@/components/ui/button";
import { NavLink } from "react-router-dom";

export default function Header() {
  const { resolvedTheme, toggleTheme } = useTheme();

  return (
    <div className="absolute  right-4 z-10 rounded-md px-4">
      <div className="flex items-center gap-1">
        <Button
          className="border-0 bg-transparent px-0.5"
          size="icon-lg"
          variant="link"
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
