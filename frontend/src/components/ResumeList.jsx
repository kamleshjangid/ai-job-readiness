import React, { useEffect, useState } from "react";
import api from "../utils/api";
import ResumeResultCard from "./ResumeResultCard";

export default function ResumeList() {
  const [resumes, setResumes] = useState([]);

  const load = async () => {
    const r = await api.get("/resumes/mine");
    setResumes(r.data);
  };

  useEffect(() => {
    load();
    const interval = setInterval(load, 5000); // poll every 5s for status updates
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h3>Your uploads</h3>
      <div>
        {resumes.length === 0 && <p>No resumes yet</p>}
        {resumes.map(r => <ResumeResultCard key={r.id} resume={r} />)}
      </div>
    </div>
  );
}
