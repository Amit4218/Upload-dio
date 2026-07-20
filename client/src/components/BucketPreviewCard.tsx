import { useState } from "react";
import { Badge } from "./ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Check, Copy } from "lucide-react";
import { HoverCard, HoverCardContent, HoverCardTrigger } from "./ui/hover-card";
import { Label } from "./ui/label";

interface BucketPreviewCardProps {
  name?: string;
  publicId?: string;
  totalFiles?: number;
  fileTypes?: {
    images: number;
    videos: number;
    audios: number;
    others: number;
  };
  allocatedSpace?: number; // in GB
  usedSpace?: number; // in GB
}

export function BucketPreviewCard({
  name = "BUCKET NAME",
  publicId = "#34abeR",
  totalFiles = 35,
  fileTypes = { images: 5, videos: 10, audios: 10, others: 10 },
  allocatedSpace = 24,
  usedSpace = 10,
}: BucketPreviewCardProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(publicId);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy ID: ", err);
    }
  };

  const usedPercentage = Math.min((usedSpace / allocatedSpace) * 100, 100);

  return (
    <Card className="w-full border shadow-sm flex flex-col justify-between mb-3">
      <div>
        <CardHeader className="px-2 flex flex-row items-center justify-between -mt-5">
          <CardTitle className="px-2 text-base font-semibold tracking-tight truncate max-w-45">
            {name}
          </CardTitle>
          <HoverCard>
            <HoverCardTrigger>
              <Button
                variant="outline"
                size="sm"
                className="h-7 px-2 text-xs gap-1.5 font-normal text-muted-foreground hover:text-foreground"
                onClick={handleCopy}
              >
                <span className="font-mono truncate max-w-15">{publicId}</span>
                {copied ? (
                  <Check size={13} className="text-green-500" />
                ) : (
                  <Copy size={13} />
                )}
              </Button>
            </HoverCardTrigger>
            <HoverCardContent className={"w-25"}>
              <Label>click to copy public id</Label>
            </HoverCardContent>
          </HoverCard>
        </CardHeader>

        <CardContent className="p-4 pt-2 space-y-4">
          {/* Quick Stats Banner */}
          <div className="flex items-center justify-between text-xs border-b pb-2">
            <span className="text-muted-foreground">Total Files</span>
            <span className="font-medium font-mono">{totalFiles}</span>
          </div>

          {/* Breakdown by File Type */}
          <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-xs">
            <div className="flex justify-between items-center">
              <span className="text-muted-foreground">Images</span>
              <Badge
                variant="secondary"
                className="h-5 px-1.5 text-[10px] font-mono"
              >
                {fileTypes.images}
              </Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-muted-foreground">Videos</span>
              <Badge
                variant="secondary"
                className="h-5 px-1.5 text-[10px] font-mono"
              >
                {fileTypes.videos}
              </Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-muted-foreground">Audio</span>
              <Badge
                variant="secondary"
                className="h-5 px-1.5 text-[10px] font-mono"
              >
                {fileTypes.audios}
              </Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-muted-foreground">Others</span>
              <Badge
                variant="secondary"
                className="h-5 px-1.5 text-[10px] font-mono"
              >
                {fileTypes.others}
              </Badge>
            </div>
          </div>

          {/* Storage Section with Dynamic Visualization */}
          <div className="space-y-1.5 pt-1">
            <div className="flex justify-between text-xs font-medium">
              <span className="text-muted-foreground">Storage</span>
              <span>
                {usedSpace}GB{" "}
                <span className="text-muted-foreground font-normal">
                  / {allocatedSpace}GB
                </span>
              </span>
            </div>
            {/* Visual Storage Bar */}
            <HoverCard>
              <HoverCardTrigger>
                <div className="w-full bg-secondary h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-primary h-full transition-all duration-300"
                    style={{ width: `${usedPercentage}%` }}
                  />
                </div>
              </HoverCardTrigger>
              <HoverCardContent className={"max-w-20 p-0 px-2"}>
                <Badge>
                  {usedSpace} / {allocatedSpace} GB
                </Badge>
              </HoverCardContent>
            </HoverCard>
          </div>
        </CardContent>
      </div>

      <div className="flex gap-3 px-4 -mt-6">
        <Button size="sm">View contents</Button>
        <Button size="sm">Edit / View Configurations</Button>
      </div>
    </Card>
  );
}

export default BucketPreviewCard;
