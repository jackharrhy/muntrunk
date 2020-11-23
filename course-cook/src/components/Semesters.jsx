import React, { useEffect } from 'react';
import { useQuery } from 'urql';
import { Select } from 'evergreen-ui'

const converter = (data) => {
  return data.semester.map((node) => {
    const {year, term, level} = node;
    node.label = `${year}-${year+1} ${term === 1 ? 'Fall' : 'Winter'} (${level === 1 ? 'Undergrad' : 'Graduate'})`;
    return node;
  });
};

export default function Semesters({semesterId, setSemesterId}) {
	const [res] = useQuery({
		query: `
      query AllSemesters {
        semester {
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
    <Select
      height="3rem"
      padding="1rem"
      value={semesterId}
      onChange={(event) => setSemesterId(event.target.value)}
    >
      {
        semesters.reverse().map((semester) => (
          <option key={semester.id} value={semester.id}>{semester.label}</option>
        ))
      }
    </Select>
  );
}
