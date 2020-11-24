import React from "react";
import { useQuery } from "urql";

export default function Subjects({ subjectId, setSubjectId }) {
  const [res] = useQuery({
    query: `
      query AllSubjects {
        subject {
          id
          name
        }
      }
    `,
  });

  if (res.fetching) return <p>Loading...</p>;
  if (res.error) return <p>Errored!</p>;

  return (
    <select
      value={subjectId}
      onChange={(event) => setSubjectId(event.target.value === "" ? "" : parseInt(event.target.value, 10))}
    >
      <option value={""}>Select a subject...</option>
      {res.data.subject.map(({ id, name }) => (
        <option key={id} value={id}>
          {name}
        </option>
      ))}
    </select>
  );
}
