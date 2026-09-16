import { useState } from "react";
import axios from "axios";
import ChatWindow from "./components/ChatWindow";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (event) => {
    event.preventDefault();
    if (!message.trim()) return;
    setLoading(true);
    try {
      const { data } = await axios.get("/api/chat", { params: { message } });
      setResponse(data.response || "");
      setCourses(data.courses || []);
    } catch (error) {
      setResponse(error.response?.data?.detail || "Unable to reach the learning assistant.");
      setCourses([]);
    } finally {
      setLoading(false);
    }
  };

  const showDetails = (course) => {
    setResponse(`${course.title} is a ${course.level} course with approximately ${course.durationHours} hours of learning.`);
  };

  const enroll = async (course) => {
    setLoading(true);
    try {
      const { data } = await axios.get("/api/chat", {
        params: { message: `enroll ${course.learningId}` },
      });
      setResponse(data.response || `Enrolled in ${course.title}.`);
    } catch (error) {
      setResponse(error.response?.data?.detail || "Unable to enroll in this course.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="app-shell">
      <div className="ambient-shape ambient-shape-one" />
      <div className="ambient-shape ambient-shape-two" />
      <ChatWindow
        message={message}
        setMessage={setMessage}
        onSubmit={sendMessage}
        loading={loading}
        response={response}
        courses={courses}
        onDetails={showDetails}
        onEnroll={enroll}
      />
    </main>
  );
}

export default App;
