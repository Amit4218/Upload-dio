import { useState } from "react";
import { Switch } from "@/components/ui/switch";

interface UploadConfig {
  bucket_name: string;
  allowed_origin: string;
  maxfiles: number;
  save_folder_path: string;
  include_videos: boolean;
  include_files: boolean;
  include_audio: boolean;
  callback_url: string;
  image_settings: {
    modify_image: boolean;
    resize: {
      resize_image: boolean;
      height: number;
      width: number;
    };
    compress_image: boolean;
    change_file_ext: {
      change_file_ext: boolean;
      ext: string;
    };
  };
}

const defaultConfig: UploadConfig = {
  bucket_name: "",
  allowed_origin: "",
  maxfiles: 1,
  save_folder_path: "",
  include_videos: false,
  include_files: false,
  include_audio: false,
  callback_url: "",
  image_settings: {
    modify_image: true,
    resize: {
      resize_image: false,
      height: 0,
      width: 0,
    },
    compress_image: false,
    change_file_ext: {
      change_file_ext: false,
      ext: "webp",
    },
  },
};

export default function UploadConfigModal() {
  const [config, setConfig] = useState<UploadConfig>(defaultConfig);

  return (
    <div className="fixed inset-0 z-20 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="w-full max-w-3xl rounded-xl bg-white p-6 shadow-2xl overflow-y-auto max-h-[90vh]">
        <h2 className="text-2xl font-bold mb-6">Upload Configuration</h2>

        <div className="grid grid-cols-2 gap-4">
          <Input
            label="Bucket Name"
            value={config.bucket_name}
            onChange={(v) => setConfig({ ...config, bucket_name: v })}
          />

          <Input
            label="Allowed Origin"
            value={config.allowed_origin}
            onChange={(v) => setConfig({ ...config, allowed_origin: v })}
          />

          <Input
            label="Save Folder"
            value={config.save_folder_path}
            onChange={(v) => setConfig({ ...config, save_folder_path: v })}
          />

          <Input
            label="Callback URL"
            value={config.callback_url}
            onChange={(v) => setConfig({ ...config, callback_url: v })}
          />

          <Input
            type="number"
            label="Max Files"
            value={config.maxfiles}
            onChange={(v) =>
              setConfig({
                ...config,
                maxfiles: Number(v),
              })
            }
          />
        </div>

        <div className="mt-8 space-y-4">
          <SwitchRow
            label="Include Videos"
            checked={config.include_videos}
            onCheckedChange={(checked) =>
              setConfig({
                ...config,
                include_videos: checked,
              })
            }
          />

          <SwitchRow
            label="Include Files"
            checked={config.include_files}
            onCheckedChange={(checked) =>
              setConfig({
                ...config,
                include_files: checked,
              })
            }
          />

          <SwitchRow
            label="Include Audio"
            checked={config.include_audio}
            onCheckedChange={(checked) =>
              setConfig({
                ...config,
                include_audio: checked,
              })
            }
          />
        </div>

        <div className="mt-10 rounded-lg border p-5 space-y-5">
          <h3 className="font-semibold text-lg">Image Settings</h3>

          <SwitchRow
            label="Modify Image"
            checked={config.image_settings.modify_image}
            onCheckedChange={(checked) =>
              setConfig({
                ...config,
                image_settings: {
                  ...config.image_settings,
                  modify_image: checked,
                },
              })
            }
          />

          <SwitchRow
            label="Compress Image"
            checked={config.image_settings.compress_image}
            onCheckedChange={(checked) =>
              setConfig({
                ...config,
                image_settings: {
                  ...config.image_settings,
                  compress_image: checked,
                },
              })
            }
          />

          <div className="rounded-md border p-4 space-y-4">
            <SwitchRow
              label="Resize Image"
              checked={config.image_settings.resize.resize_image}
              onCheckedChange={(checked) =>
                setConfig({
                  ...config,
                  image_settings: {
                    ...config.image_settings,
                    resize: {
                      ...config.image_settings.resize,
                      resize_image: checked,
                    },
                  },
                })
              }
            />

            {config.image_settings.resize.resize_image && (
              <div className="grid grid-cols-2 gap-4">
                <Input
                  type="number"
                  label="Width"
                  value={config.image_settings.resize.width}
                  onChange={(v) =>
                    setConfig({
                      ...config,
                      image_settings: {
                        ...config.image_settings,
                        resize: {
                          ...config.image_settings.resize,
                          width: Number(v),
                        },
                      },
                    })
                  }
                />

                <Input
                  type="number"
                  label="Height"
                  value={config.image_settings.resize.height}
                  onChange={(v) =>
                    setConfig({
                      ...config,
                      image_settings: {
                        ...config.image_settings,
                        resize: {
                          ...config.image_settings.resize,
                          height: Number(v),
                        },
                      },
                    })
                  }
                />
              </div>
            )}
          </div>

          <div className="rounded-md border p-4 space-y-4">
            <SwitchRow
              label="Change File Extension"
              checked={config.image_settings.change_file_ext.change_file_ext}
              onCheckedChange={(checked) =>
                setConfig({
                  ...config,
                  image_settings: {
                    ...config.image_settings,
                    change_file_ext: {
                      ...config.image_settings.change_file_ext,
                      change_file_ext: checked,
                    },
                  },
                })
              }
            />

            {config.image_settings.change_file_ext.change_file_ext && (
              <Input
                label="Extension"
                value={config.image_settings.change_file_ext.ext}
                onChange={(v) =>
                  setConfig({
                    ...config,
                    image_settings: {
                      ...config.image_settings,
                      change_file_ext: {
                        ...config.image_settings.change_file_ext,
                        ext: v,
                      },
                    },
                  })
                }
              />
            )}
          </div>
        </div>

        <button
          className="mt-8 w-full rounded-lg bg-blue-600 py-3 text-white font-medium hover:bg-blue-700"
          onClick={() => console.log(config)}
        >
          Save Configuration
        </button>
      </div>
    </div>
  );
}

interface InputProps {
  label: string;
  value: string | number;
  onChange: (value: string) => void;
  type?: string;
}

function Input({ label, value, onChange, type = "text" }: InputProps) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-sm font-medium">{label}</label>
      <input
        type={type}
        value={value}
        className="rounded-md border px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500"
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}

interface SwitchRowProps {
  label: string;
  checked: boolean;
  onCheckedChange: (checked: boolean) => void;
}

function SwitchRow({ label, checked, onCheckedChange }: SwitchRowProps) {
  return (
    <div className="flex items-center justify-between rounded-md border p-3">
      <span>{label}</span>
      <Switch checked={checked} onCheckedChange={onCheckedChange} />
    </div>
  );
}
