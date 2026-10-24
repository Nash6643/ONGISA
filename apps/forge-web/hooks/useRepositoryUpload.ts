import { useState } from 'react';

export function useRepositoryUpload() {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const uploadZip = async (file: File) => {
    setIsUploading(true);
    setUploadError(null);
    try {
      // Simulation or API trigger wrapper
      await new Promise((res) => setTimeout(res, 1000));
    } catch (err: any) {
      setUploadError(err.message || 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  return { isUploading, uploadError, uploadZip };
}