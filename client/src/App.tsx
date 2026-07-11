import { Route, Routes } from "react-router-dom";
import { Toaster } from "@/components/ui/sonner";
import AuthLayout from "@/layouts/AuthLayout";
import DashboardLayout from "@/layouts/DashboardLayout";
import Login from "@/pages/auth/Login";
import Dashboard from "@/pages/dashboard/Dashboard";
import BucketsPreview from "@/pages/dashboard/BucketsPreview";
import Settings from "@/pages/dashboard/Settings";
import NotFound from "@/pages/NotFound";
import Profile from "@/pages/dashboard/Profile";

function App() {
  return (
    <>
      <Routes>
        <Route path="/auth" element={<AuthLayout />}>
          <Route path="login" element={<Login />} />
        </Route>

        <Route path="/dashboard" element={<DashboardLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="buckets" element={<BucketsPreview />} />
          <Route path="settings" element={<Settings />} />
          <Route path="profile" element={<Profile />} />
        </Route>

        <Route path="*" element={<NotFound />} />
      </Routes>

      <Toaster position="top-right" />
    </>
  );
}

export default App;
