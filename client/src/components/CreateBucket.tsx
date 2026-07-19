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

interface UploadConfigModalProps {
  open: boolean;
  onClose: () => void;
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

export default function UploadConfigModal({
  open,
  onClose,
}: UploadConfigModalProps) {
  const [config, setConfig] = useState<UploadConfig>(defaultConfig);

  if (!open) return null;

  return (
    <div
      onClick={onClose}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="w-full max-w-4xl max-h-[85vh] flex flex-col rounded-xl bg-background text-foreground shadow-2xl border border-border"
      >
        {/* Header */}
        <div className="p-6 border-b border-border">
          <h2 className="text-xl font-semibold tracking-tight">
            Upload Configuration
          </h2>
          <p className="text-sm text-muted-foreground mt-1">
            Manage bucket settings, media allowances, and image transformations.
          </p>
        </div>

        {/* Content Columns */}
        <div className="flex-1 overflow-y-auto p-6 grid grid-cols-1 md:grid-cols-2 gap-8 bg-muted/20">
          {/* Left Column: Core Settings */}
          <div className="space-y-6">
            <div>
              <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-4">
                Core Settings
              </h3>
              <div className="space-y-4 bg-background p-5 rounded-xl border border-border shadow-sm">
                <Input
                  label="Bucket Name"
                  placeholder="e.g. production-assets"
                  value={config.bucket_name}
                  onChange={(v) => setConfig({ ...config, bucket_name: v })}
                />
                <Input
                  label="Allowed Origin"
                  placeholder="https://example.com"
                  value={config.allowed_origin}
                  onChange={(v) => setConfig({ ...config, allowed_origin: v })}
                />
                <Input
                  label="Save Folder Path"
                  placeholder="e.g. /uploads/images"
                  tooltip="Target destination directory, directorys will be created in ~/Uploadio"
                  value={config.save_folder_path}
                  onChange={(v) =>
                    setConfig({ ...config, save_folder_path: v })
                  }
                />
                <Input
                  label="Callback URL"
                  placeholder="https://api.example.com/webhook"
                  tooltip="Sends the uploaded files urls after process completion"
                  value={config.callback_url}
                  onChange={(v) => setConfig({ ...config, callback_url: v })}
                />
                <Input
                  type="number"
                  label="Max Files Per Upload"
                  tooltip="Restricts total concurrent payloads allowed within a single upload action."
                  value={config.maxfiles}
                  onChange={(v) =>
                    setConfig({ ...config, maxfiles: Number(v) })
                  }
                />
              </div>
            </div>

            <div>
              <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-4">
                Allowed Media Types
              </h3>
              <div className="divide-y divide-border bg-background rounded-xl border border-border shadow-sm overflow-hidden">
                <SwitchRow
                  label="Include Videos"
                  description="Allow users to upload mp4, mov, and webm files."
                  checked={config.include_videos}
                  onCheckedChange={(checked) =>
                    setConfig({ ...config, include_videos: checked })
                  }
                />
                <SwitchRow
                  label="Include Files"
                  description="Allow documents, PDFs, and compressed archives."
                  checked={config.include_files}
                  onCheckedChange={(checked) =>
                    setConfig({ ...config, include_files: checked })
                  }
                />
                <SwitchRow
                  label="Include Audio"
                  description="Allow mp3, wav, and ogg formats."
                  checked={config.include_audio}
                  onCheckedChange={(checked) =>
                    setConfig({ ...config, include_audio: checked })
                  }
                />
              </div>
            </div>
          </div>

          {/* Right Column: Processing Pipelines */}
          <div className="space-y-6">
            <div>
              <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-4">
                Image Processing Engine
              </h3>
              <div className="space-y-4 bg-background p-5 rounded-xl border border-border shadow-sm">
                <SwitchRow
                  label="Modify Image Pipeline"
                  description="Master switch to toggle all post-processing rules."
                  tooltip="Disabling this completely bypasses size reductions and conversions."
                  checked={config.image_settings.modify_image}
                  noBorder
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

                {config.image_settings.modify_image && (
                  <div className="pt-4 border-t border-border space-y-4">
                    <SwitchRow
                      label="Compress Image"
                      description="Reduce file sizes without noticeable quality loss."
                      checked={config.image_settings.compress_image}
                      noBorder
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

                    {/* Resize Box */}
                    <div className="p-3 bg-muted/30 rounded-lg border border-border space-y-3">
                      <SwitchRow
                        label="Resize Image"
                        description="Enforce maximum pixel dimensions."
                        checked={config.image_settings.resize.resize_image}
                        noBorder
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
                        <div className="grid grid-cols-2 gap-3 pt-2">
                          <Input
                            type="number"
                            label="Width (px)"
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
                            label="Height (px)"
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

                    {/* Format Conversion Box */}
                    <div className="p-3 bg-muted/30 rounded-lg border border-border space-y-3">
                      <SwitchRow
                        label="Convert File Format"
                        description="Force change format during optimization."
                        checked={
                          config.image_settings.change_file_ext.change_file_ext
                        }
                        noBorder
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
                      {config.image_settings.change_file_ext
                        .change_file_ext && (
                        <Input
                          label="Target Extension"
                          placeholder="e.g. webp, avif"
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
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-border flex items-center justify-end gap-3 bg-background">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium rounded-lg border border-input bg-background hover:bg-accent hover:text-accent-foreground transition-colors"
          >
            Cancel
          </button>
          <button
            className="px-5 py-2 text-sm font-medium text-primary-foreground bg-primary hover:bg-primary/90 rounded-lg shadow-sm transition-colors"
            onClick={() => {
              console.log(config);
              onClose();
            }}
          >
            Create bucket
          </button>
        </div>
      </div>
    </div>
  );
}

{
  /* Micro Tooltip UI element built using core utility positioning */
}
function InfoTooltip({ text }: { text: string }) {
  return (
    <div className="group relative inline-block ml-1.5 cursor-help">
      <svg
        className="h-3.5 w-3.5 text-muted-foreground/70 hover:text-muted-foreground"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        strokeWidth={2.5}
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z"
        />
      </svg>
      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block w-48 rounded bg-popover border border-border p-2 text-xs font-normal text-popover-foreground shadow-md z-30 leading-normal pointer-events-none">
        {text}
      </div>
    </div>
  );
}

interface InputProps {
  label: string;
  value: string | number;
  onChange: (value: string) => void;
  type?: string;
  placeholder?: string;
  tooltip?: string;
}

function Input({
  label,
  value,
  onChange,
  type = "text",
  placeholder,
  tooltip,
}: InputProps) {
  return (
    <div className="flex flex-col gap-1.5">
      <div className="flex items-center">
        <label className="text-xs font-semibold tracking-wide text-foreground/80">
          {label}
        </label>
        {tooltip && <InfoTooltip text={tooltip} />}
      </div>
      <input
        type={type}
        value={value === 0 ? "" : value}
        placeholder={placeholder}
        className="w-full rounded-lg border border-input bg-background px-3 py-2 text-sm text-foreground outline-none transition-all placeholder:text-muted-foreground/60 focus:ring-2 focus:ring-ring/20 focus:border-ring"
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}

interface SwitchRowProps {
  label: string;
  description?: string;
  checked: boolean;
  onCheckedChange: (checked: boolean) => void;
  noBorder?: boolean;
  tooltip?: string;
}

function SwitchRow({
  label,
  description,
  checked,
  onCheckedChange,
  noBorder = false,
  tooltip,
}: SwitchRowProps) {
  return (
    <div
      className={`flex items-start justify-between p-4 ${noBorder ? "p-0" : ""}`}
    >
      <div className="flex flex-col gap-0.5 pr-4">
        <div className="flex items-center">
          <span className="text-sm font-medium text-foreground">{label}</span>
          {tooltip && <InfoTooltip text={tooltip} />}
        </div>
        {description && (
          <span className="text-xs text-muted-foreground leading-normal">
            {description}
          </span>
        )}
      </div>
      <div className="flex items-center h-5">
        <Switch checked={checked} onCheckedChange={onCheckedChange} />
      </div>
    </div>
  );
}
