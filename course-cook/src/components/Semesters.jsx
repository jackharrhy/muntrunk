import React from "react";
import { useQuery } from "urql";

const converter = (data) => {
  return data.semester.map((node) => {
    const { year, term, level } = node;
    node.label = `${year}-${year + 1} ${term === 1 ? "Fall" : "Winter"} (${
      level === 1 ? "Undergrad" : "Graduate"
    })`;
    return node;
  });
};

export default function Semesters({ semesterId, setSemesterId }) {
  const [res] = useQuery({
    query: `
      query AllSemesters {
        semester(order_by: {id: desc}) {
          id
          year
          term
          level
        }
      }
    `,
  });

  if (res.fetching) return <p>Loading...</p>;
  if (res.error) return <p>Errored!</p>;

  const semesters = converter(res.data);

  return (
    <select
      value={semesterId}
      onChange={(event) => setSemesterId(parseInt(event.target.value, 10))}
    >
      <option value={""}>Select a semester...</option>
      {semesters.map(({ id, label }) => (
        <option key={id} value={id}>
          {label}
        </option>
      ))}
    </select>
  );
}
