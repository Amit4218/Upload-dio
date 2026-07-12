import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  LayoutDashboard,
  Settings,
  ChevronsUpDown,
  LogOut,
  User,
  PackageOpen,
} from "lucide-react";
import { NavLink } from "react-router-dom";
import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar";

const NAVIGATION_LINKS = [
  { link: "/dashboard", tooktip: "Dashboard", icon: LayoutDashboard },
  { link: "/dashboard/buckets", tooktip: "Bucket Previews", icon: PackageOpen },
  { link: "/dashboard/settings", tooktip: "Settings", icon: Settings },
];

function AppSidebar() {
  return (
    <Sidebar variant="sidebar" collapsible="icon">
      {/* Header */}
      <SidebarHeader className="border-b">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              render={<NavLink to="/dashboard" />}
              size="sm"
              tooltip="Dashboard"
            >
              <img
                src="/logo.png"
                alt="Uploadio"
                className="h-6 w-6 rounded-md object-contain"
              />
              <span className="font-semibold text-lg">Uploadio</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>

      {/* Navigation */}
      <SidebarContent>
        <SidebarGroup>
          <SidebarMenu>
            {NAVIGATION_LINKS.map((element, idx) => (
              <SidebarMenuItem key={idx}>
                <SidebarMenuButton
                  render={<NavLink to={element.link} />}
                  tooltip={element.tooktip}
                >
                  <element.icon className="h-4 w-4" />
                  <span>{element.tooktip}</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            ))}
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>

      {/* Footer */}
      <SidebarFooter className="border-t">
        <SidebarMenu>
          <SidebarMenuItem>
            <DropdownMenu>
              <DropdownMenuTrigger
                render={
                  <SidebarMenuButton size="sm" tooltip="profile">
                    <Avatar size="sm">
                      <AvatarImage src="/default_profile.png" alt="Profile" />
                      <AvatarFallback>CN</AvatarFallback>
                    </Avatar>
                    <div className="flex min-w-0 flex-1 flex-col text-left">
                      <span className="truncate text-sm font-medium">
                        John Doe
                      </span>
                      <span className="truncate text-xs text-muted-foreground">
                        john@example.com
                      </span>
                    </div>

                    <ChevronsUpDown className="ml-auto h-4 w-4" />
                  </SidebarMenuButton>
                }
              />

              <DropdownMenuContent side="top" align="end" className="w-30">
                <DropdownMenuItem>
                  <NavLink className={"flex w-full"} to={"/dashboard/profile"}>
                    <User className="mr-2 h-4 w-4" />
                    Profile
                  </NavLink>
                </DropdownMenuItem>

                <DropdownMenuItem
                  className="text-red-600"
                  onClick={() => {
                    console.log("Logout");
                  }}
                >
                  <LogOut className="mr-2 h-4 w-4" />
                  Logout
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}

export default AppSidebar;
