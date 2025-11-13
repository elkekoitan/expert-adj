"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import {
  Upload,
  FileCode,
  Settings,
  TrendingUp,
  Copy,
  Star,
  Search,
} from "lucide-react";

export default function ExpertsPage() {
  const router = useRouter();
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setUploadResult(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const API_BASE =
        process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

      const response = await fetch(`${API_BASE}/eas/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const txt = await response.text();
        throw new Error(txt || "Upload failed");
      }

      const data = await response.json();

      // Beklenen normalize response:
      // {
      //   "ea": { "name": str, "platform": str, "file_size": int, "has_source": bool },
      //   "parameters": {
      //      "extracted": int,
      //      "summary": { "optimizable_count": int, "group_count": int, "groups": [...] },
      //      "details": [...]
      //   }
      // }
      // Backend farklı dönse bile, mevcut alanlar üzerinden en yakın eşleşmeyi UI'da gösteriyoruz.
      setUploadResult(data);
      setSelectedFile(null);
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Upload failed. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              Expert Advisors
            </h1>
            <p className="text-slate-400">
              Upload and manage your trading robots
            </p>
          </div>
          <button
            onClick={() => router.push("/experts/analyze")}
            className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 px-6 py-3 rounded-lg font-semibold transition-all"
          >
            <Search className="w-5 h-5" />
            Analyze EA
          </button>
        </div>

        {/* Upload Section */}
        <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-8 mb-8">
          <div className="flex items-center gap-3 mb-6">
            <Upload className="w-6 h-6 text-blue-400" />
            <h2 className="text-2xl font-semibold">Upload Expert Advisor</h2>
          </div>

          <div className="space-y-6">
            {/* File Input */}
            <div className="border-2 border-dashed border-slate-600 rounded-xl p-8 text-center hover:border-blue-500 transition-colors">
              <input
                type="file"
                id="ea-file"
                accept=".mq4,.mq5,.ex4,.ex5"
                onChange={handleFileChange}
                className="hidden"
              />
              <label htmlFor="ea-file" className="cursor-pointer">
                <FileCode className="w-16 h-16 mx-auto mb-4 text-slate-500" />
                <p className="text-lg mb-2">
                  {selectedFile ? selectedFile.name : "Click to select EA file"}
                </p>
                <p className="text-sm text-slate-400">
                  Supports .mq4, .mq5, .ex4, .ex5 files
                </p>
              </label>
            </div>

            {/* Upload Button */}
            {selectedFile && (
              <button
                onClick={handleUpload}
                disabled={uploading}
                className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:from-slate-600 disabled:to-slate-700 px-6 py-4 rounded-xl font-semibold text-lg transition-all transform hover:scale-[1.02] disabled:scale-100 disabled:cursor-not-allowed"
              >
                {uploading
                  ? "Uploading & Analyzing..."
                  : "Upload & Extract Parameters"}
              </button>
            )}
          </div>
        </div>

        {/* Upload Result */}
        {uploadResult && (
          <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-8 mb-8">
            <div className="flex items-center gap-3 mb-6">
              <Settings className="w-6 h-6 text-green-400" />
              <h2 className="text-2xl font-semibold">Upload Successful!</h2>
            </div>

            {/* EA Info */}
            <div className="bg-slate-900/50 rounded-xl p-6 mb-6">
              <h3 className="text-lg font-semibold mb-4 text-blue-400">
                EA Information
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-slate-400 text-sm">Name</p>
                  <p className="font-semibold">{uploadResult.ea.name}</p>
                </div>
                <div>
                  <p className="text-slate-400 text-sm">Platform</p>
                  <p className="font-semibold">{uploadResult.ea.platform}</p>
                </div>
                <div>
                  <p className="text-slate-400 text-sm">File Size</p>
                  <p className="font-semibold">
                    {(uploadResult.ea.file_size / 1024).toFixed(2)} KB
                  </p>
                </div>
                <div>
                  <p className="text-slate-400 text-sm">Source Code</p>
                  <p className="font-semibold">
                    {uploadResult.ea.has_source
                      ? "✓ Available"
                      : "✗ Not Available"}
                  </p>
                </div>
              </div>
            </div>

            {/* Parameters Summary */}
            {uploadResult.parameters.extracted > 0 && (
              <div className="bg-slate-900/50 rounded-xl p-6">
                <h3 className="text-lg font-semibold mb-4 text-purple-400">
                  Extracted Parameters
                </h3>

                <div className="grid grid-cols-3 gap-4 mb-6">
                  <div className="bg-slate-800 rounded-lg p-4 text-center">
                    <p className="text-3xl font-bold text-blue-400">
                      {uploadResult.parameters.extracted}
                    </p>
                    <p className="text-slate-400 text-sm">Total Parameters</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-4 text-center">
                    <p className="text-3xl font-bold text-green-400">
                      {uploadResult.parameters.summary.optimizable_count}
                    </p>
                    <p className="text-slate-400 text-sm">Optimizable</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-4 text-center">
                    <p className="text-3xl font-bold text-purple-400">
                      {uploadResult.parameters.summary.group_count}
                    </p>
                    <p className="text-slate-400 text-sm">Groups</p>
                  </div>
                </div>

                {/* Parameter Groups */}
                <div className="space-y-2 mb-6">
                  <p className="text-sm font-semibold text-slate-400 mb-2">
                    Parameter Groups:
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {uploadResult.parameters.summary.groups?.map(
                      (group: string, idx: number) => (
                        <span
                          key={idx}
                          className="bg-slate-800 px-3 py-1 rounded-full text-sm"
                        >
                          {group}
                        </span>
                      ),
                    )}
                  </div>
                </div>

                {/* Sample Parameters */}
                <div className="space-y-2">
                  <p className="text-sm font-semibold text-slate-400 mb-2">
                    Sample Parameters:
                  </p>
                  <div className="space-y-2">
                    {uploadResult.parameters.details?.map(
                      (param: any, idx: number) => (
                        <div key={idx} className="bg-slate-800 rounded-lg p-3">
                          <div className="flex justify-between items-start">
                            <div>
                              <p className="font-mono font-semibold">
                                {param.name}
                              </p>
                              <p className="text-sm text-slate-400">
                                {param.description || "No description"}
                              </p>
                            </div>
                            <div className="text-right">
                              <span className="text-xs bg-blue-500/20 text-blue-400 px-2 py-1 rounded">
                                {param.parameter_type}
                              </span>
                              <p className="text-sm mt-1 text-slate-300">
                                = {param.default_value}
                              </p>
                            </div>
                          </div>
                        </div>
                      ),
                    )}
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-4 mt-6">
                  <button className="flex-1 bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-semibold transition-colors flex items-center justify-center gap-2">
                    <Settings className="w-5 h-5" />
                    Edit Parameters
                  </button>
                  <button className="flex-1 bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-lg font-semibold transition-colors flex items-center justify-center gap-2">
                    <TrendingUp className="w-5 h-5" />
                    Start Optimization
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* EA List (Placeholder) */}
        <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-8">
          <div className="flex items-center gap-3 mb-6">
            <FileCode className="w-6 h-6 text-yellow-400" />
            <h2 className="text-2xl font-semibold">My Expert Advisors</h2>
          </div>

          <div className="text-center py-12 text-slate-400">
            <FileCode className="w-16 h-16 mx-auto mb-4 text-slate-600" />
            <p>No EAs uploaded yet. Upload your first Expert Advisor above!</p>
          </div>
        </div>
      </div>
    </div>
  );
}
