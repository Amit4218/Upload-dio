import { useState } from "react";
import UploadConfigModal from "@/components/CreateBucket";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";

function BucketsPreview() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <>
      <div className="flex justify-between items-center h-10 pb-5 border-b">
        <Label>Bucket Previews</Label>

        <Button onClick={() => setIsModalOpen(true)}>
          Create New Bucket
        </Button>
      </div>

      <UploadConfigModal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </>
  );
}

export default BucketsPreview;