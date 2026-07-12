import { useState } from "react";
import { User2 } from "lucide-react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { SidebarSeparator } from "@/components/ui/sidebar";

function Profile() {
  const [open, setOpen] = useState(false);

  return (
    <div className="flex justify-center">
      <div className="w-full max-w-3xl">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User2 className="h-5 w-5" />
              Profile
            </CardTitle>
          </CardHeader>

          <SidebarSeparator />

          <CardContent className="space-y-8">
            {/* Avatar Section */}
            <div className="flex items-center gap-6">
              <Avatar className="h-32 w-32">
                <AvatarImage src="/default_profile.png" alt="profile" />
                <AvatarFallback className="text-3xl">N/A</AvatarFallback>
              </Avatar>

              <div className="space-y-3">
                <Button className={"rounded-full"}>
                  <Label htmlFor="profile-upload" className="cursor-pointer">
                    Upload Photo
                  </Label>
                </Button>

                <Input
                  id="profile-upload"
                  type="file"
                  accept="image/*"
                  className="hidden"
                />

                <p className="ml-2 text-xs text-muted-foreground">
                  png, jpg, etc. 800x800 recommended
                </p>
              </div>
            </div>

            {/* Username */}
            <div className="space-y-2">
              <Label>Username</Label>
              <Input value="john_doe" disabled />
            </div>

            {/* Password */}
            <div className="flex items-end justify-between gap-4">
              <div className="flex-1 space-y-2">
                <Label>Password</Label>
                <Input type="password" value="************" disabled />
              </div>

              <Dialog open={open} onOpenChange={setOpen}>
                <DialogTrigger>
                  <Button variant="outline">Edit</Button>
                </DialogTrigger>

                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Confirm Password</DialogTitle>
                    <DialogDescription>
                      Enter your current password before changing it.
                    </DialogDescription>
                  </DialogHeader>

                  <div className="space-y-2">
                    <Label>Current Password</Label>
                    <Input
                      type="password"
                      placeholder="Enter current password"
                    />
                  </div>

                  <DialogFooter>
                    <Button variant="outline" onClick={() => setOpen(false)}>
                      Cancel
                    </Button>

                    <Button>Continue</Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            </div>
          </CardContent>

          <CardFooter />
        </Card>
      </div>
    </div>
  );
}

export default Profile;
