import React from "react";
import { cn } from "@/lib/utils";

// Message Component (incoming and outgoing)
const Message = ({ message, type = "incoming" }) => {
  const isOutgoing = type === "outgoing";

  return (
    <div
      className={cn(
        "flex items-start space-x-3 my-2",
        isOutgoing ? "justify-end" : "justify-start"
      )}
    >
      {!isOutgoing && (
        <div className="w-8 h-8 rounded-full bg-gray-300 flex-shrink-0" />
      )}
      <div
        className={cn(
          "max-w-xs px-4 py-2 rounded-lg shadow-md bg-gray-300 text-black"
        )}
      >
        {message}
      </div>
      {isOutgoing && (
        <div className="w-8 h-8 rounded-full bg-gray-300 text-white flex-shrink-0 flex items-center justify-center">
          {/* Optional avatar for the outgoing message */}
        </div>
      )}
    </div>
  );
};

export { Message };
