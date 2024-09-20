"use client";

import React, { useState } from "react";
import { Textarea } from "./textarea";
import { Chatbox } from "./chatbox";
import { Button } from "./button";

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    { text: "Hi, how can I help you?", type: "incoming" },
    { text: "I'm looking for some information.", type: "outgoing" }
  ]);
  const [newMessage, setNewMessage] = useState("");

  const handleSendMessage = () => {
    if (newMessage.trim() === "") return;

    setMessages([...messages, { text: newMessage, type: "outgoing" }]);
    setNewMessage(""); // Clear the textarea after sending
  };

  return (
    <div className="flex flex-col w-[90%] h-vh mx-auto">
      <Chatbox messages={messages} />
      <div className="p-4 flex justify-center items-center gap-2">
        <Textarea
          className="w-full"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type your message..."
        />
        <Button
          onClick={handleSendMessage}
          className="mt-2"
        >
          Send
        </Button>
      </div>
    </div>
  );
};

export default ChatInterface;  // <-- Ensure default export
