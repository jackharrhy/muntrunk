import React from "react";

import Slot from "./Slot";

export default function Section({ crn, primary, secondary, meta, slots }) {
  return (
    <div className="section">
      <p className="title">{`${crn} - ${primary ?? '?'} ${secondary ? `(${secondary})` : '' }`}</p>
      {meta.map((line) => <p key={line} className="meta">{line}</p>)}
      {slots.map((slot) => (
        <Slot
          key={slot.id}
          building={slot.building?.letter}
          room={slot.room?.number}
          begin={slot.begin}
          end={slot.end}
          daysOfWeek={slot.days_of_week}
        />
      ))}
    </div>
  );
}
