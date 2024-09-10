import React, { useEffect, useRef } from "react";
import { Message } from "./message";

const Chatbox = ({ messages }) => {
  const messageEndRef = useRef(null);

  // Auto-scroll to the bottom when a new message is added
  useEffect(() => {
    if (messageEndRef.current) {
      messageEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  return (
    <div className="flex flex-col h-full w-full overflow-y-auto p-4">
      {messages.map((msg, index) => (
        <Message key={index} message={msg.text} type={msg.type} />
      ))}
      <div ref={messageEndRef} />
    </div>
  );
};

export { Chatbox };
