import { useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  const sendMessage = async () => {
    try {
      const res = await axios.get("/api/chat", {
        params: {
          message,
        },
      });

      setResponse(res.data.response);
    } catch (error) {
      setResponse("Error connecting to backend");
      console.error(error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>MiniLearn Agent</h1>

      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask something..."
        style={{
          width: "300px",
          padding: "10px",
        }}
      />

      <button
        onClick={sendMessage}
        style={{
          marginLeft: "10px",
          padding: "10px",
        }}
      >
        Send
      </button>

      <hr />

      <div>
        {response}
      </div>
    </div>
  );
}

export default App;