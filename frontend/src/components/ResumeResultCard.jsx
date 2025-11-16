import React from "react";
import { RadialBarChart, RadialBar, Legend } from 'recharts';

export default function ResumeResultCard({ resume }) {
  const score = resume.score || {};
  const data = [
    { name: 'Overall', value: score.overall_score || 0, fill: '#8884d8' }
  ];
  return (
    <div style={{ border: "1px solid #eee", padding: 12, borderRadius: 8, marginBottom: 12 }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <div>
          <strong>{resume.filename}</strong>
          <div>Status: {resume.status}</div>
        </div>
        <div style={{ width: 120, height: 120 }}>
          {resume.status === "done" ? (
            <RadialBarChart width={120} height={120} innerRadius="20%" outerRadius="100%" data={data}>
              <RadialBar minAngle={15} background clockWise dataKey="value" />
              <Legend />
            </RadialBarChart>
          ) : <div style={{ padding: 24 }}>{resume.status}</div>}
        </div>
      </div>
      {score.details && (
        <div style={{ marginTop: 8 }}>
          <div><strong>Strengths:</strong> {(score.details.strengths || []).join(", ")}</div>
          <div><strong>Improvements:</strong> {(score.details.improvements || []).join(", ")}</div>
        </div>
      )}
    </div>
  );
}
