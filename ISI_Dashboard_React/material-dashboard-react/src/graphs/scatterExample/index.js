// import React from "react";
import React, { useState, useEffect } from "react";
import Plot from "react-plotly.js";

const defaultMessage = {
  x: [1, 2, 3],
  y: [1, 2, 3],
};

const ScatterExample = () => {
  // const [messages, setMessages] = useState([]);
  // const [message, setMessage] = useState('');
  const [message, setMessage] = useState(defaultMessage);
  const [ws, setWs] = useState(null);
  const [clientId, setClientId] = useState("");

  useEffect(() => {
    const websocket = new WebSocket("ws://127.0.0.1:8000/ws");

    websocket.onopen = () => {
      console.log("WebSocket is connected");
      // Generate a unique client ID
      const id = Math.floor(Math.random() * 1000);
      setClientId(id);
    };

    // websocket.onmessage = (evt) => {
    //     const message = (evt.data);
    //     setMess
    //     setMessages((prevMessages) =>
    //         [...prevMessages, message]);
    // };

    websocket.onmessage = (e) => {
      setMessage(JSON.parse(e.data));
    };

    websocket.onclose = () => {
      console.log("WebSocket is closed");
    };

    setWs(websocket);

    return () => {
      websocket.close();
    };
  }, []);

  // const sendMessage = () => {
  //     if (ws) {
  //         ws.send(JSON.stringify({
  //             type: 'message',
  //             payload: message,
  //             clientId: clientId
  //         }));
  //         setMessage('');
  //     }
  // };

  //   const handleInputChange = (event) => {
  //     setMessage(event.target.value);
  //   };

  return (
    <Plot
      data={[
        {
          x: message.x,
          y: message.y,
          type: "scatter",
          mode: "lines+markers",
          marker: { color: "red" },
        },
        { type: "bar", x: [1, 2, 3], y: [2, 5, 3] },
      ]}
      layout={{ width: 400, height: 400, title: "A Fancy Plot" }}
    />
  );
};

//   return (
//     <div>
//       <h1>Real-time Updates with WebSockets and React Hooks - Client {clientId}</h1>
//       {messages.map((message, index) => (
//         <p key={index}>{message}</p>
//       ))}
//       <input type="text" value={message} onChange={handleInputChange} />
//       <button onClick={sendMessage}>Send Message</button>
//     </div>
//   );

export default ScatterExample;

// function ScatterExample() {
//   //   const { sales, tasks } = reportsLineChartData;

//   return (
//     <Plot
//       data={[
//         {
//           x: [1, 2, 3],
//           y: [2, 6, 3],
//           type: "scatter",
//           mode: "lines+markers",
//           marker: { color: "red" },
//         },
//         { type: "bar", x: [1, 2, 3], y: [2, 5, 3] },
//       ]}
//       layout={{ width: 400, height: 400, title: "A Fancy Plot" }}
//     />
//   );
// }

// export default ScatterExample;
