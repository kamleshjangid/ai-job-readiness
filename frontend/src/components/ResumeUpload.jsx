import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import api from "../utils/api";

export default function ResumeUpload({ onUploaded }) {
  const [loading, setLoading] = useState(false);
  const onDrop = useCallback(async acceptedFiles => {
    const file = acceptedFiles[0];
    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);
    try {
      const res = await api.post("/resumes/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      onUploaded && onUploaded(res.data.resume_id);
    } catch (err) {
      console.error(err);
      alert(err?.response?.data?.detail || "Upload failed");
    } finally {
      setLoading(false);
    }
  }, [onUploaded]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop, maxFiles: 1,
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"]
    }
  });

  return (
    <div {...getRootProps()} style={styles.drop}>
      <input {...getInputProps()} />
      <div>
        {loading ? <p>Uploading…</p> : (isDragActive ? <p>Drop file here</p> : <p>Drag & drop resume (PDF/DOCX) or click to browse</p>)}
      </div>
    </div>
  );
}

const styles = {
  drop: { border: "2px dashed #ddd", padding: 24, borderRadius: 8, cursor: "pointer" }
};
