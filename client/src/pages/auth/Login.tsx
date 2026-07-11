import Loader from "@/components/Loader";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { login } from "@/api/auth";
import { toast } from "sonner";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handelLoginSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await login(username, password);
      toast.success("Login successful!");
      navigate("/dashboard");
    } catch (error) {
      if (axios.isAxiosError(error)) {
        toast.error(error.response?.data?.detail ?? "Login failed");
      } else {
        toast.error("Something went wrong");
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Loader />;
  }

  return (
    <div className="flex mt-16 items-center justify-center p-2">
      <div className="w-full max-w-md space-y-8">
        <div className="space-y-4 text-center">
          <img
            src="/logo.png"
            alt="uplodio logo"
            className="mx-auto h-15 w-auto"
          />

          <h1 className="text-2xl font-bold tracking-tight">
            Login to your account
          </h1>
        </div>

        <form onSubmit={handelLoginSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="username">Email address</Label>

            <Input
              id="username"
              name="username"
              type="email"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="off"
              placeholder="example@example.com"
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>

            <Input
              id="password"
              name="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              placeholder="••••••••••••••••"
              required
            />
          </div>

          <Button type="submit" className="w-full">
            Login
          </Button>
        </form>
      </div>
    </div>
  );
}
