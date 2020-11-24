import React from "react";

export default function Slot({ building, room, begin, end, daysOfWeek}) {
  const area = building ? `${building}${room} |` : '';

  return (
    <div className="slot">
      <p className="title">{`${area} ${begin} > ${end} | ${daysOfWeek}`}</p>
    </div>
  );
}
