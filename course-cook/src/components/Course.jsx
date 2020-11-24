import React, { useState } from "react";
import Sections from "./Sections";

export default function Course({ id, number, name, campus }) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <>
      <div className="course">
        <button onClick={() => setIsExpanded(!isExpanded)}>{isExpanded ? "▲": "▼"}</button>
        <p className="name">{`(${campus}) ${number} - ${name}`}</p>
      </div>
      <div className="expanded">
        {isExpanded && (
          <Sections courseId={id} />
        )}
      </div>
    </>
  );
}
