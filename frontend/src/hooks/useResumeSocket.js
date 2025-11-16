import { useEffect } from "react";

export default function useResumeSocket(onMessage) {
  useEffect(() => {
    const wsUrl = (process.env.REACT_APP_WS_URL || "ws://localhost:8000/ws/resumes");
    const ws = new WebSocket(wsUrl);
    ws.onopen = () => console.log("ws open");
    ws.onmessage = e => {
      const msg = JSON.parse(e.data);
      onMessage && onMessage(msg);
    };
    ws.onerror = e => console.error(e);
    return () => ws.close();
  }, [onMessage]);
}
