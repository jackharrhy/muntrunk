import React from "react";
import { useQuery } from "urql";

import Course from "./Course";

export default function Courses({ semesterId, subjectId }) {
  const [res] = useQuery({
    query: `
      query Courses($semesterId: Int!, $subjectId: Int!) {
        course(where: {semester_id: {_eq: $semesterId}, subject_id: {_eq: $subjectId}}) {
          id
          number
          name
          campus {
            name
          }
        }
      }
    `,
    variables: { semesterId, subjectId },
  });

  if (res.fetching) return <p>Loading...</p>;
  if (res.error) return <p>Errored!</p>;

  return res.data.course.map((course) => <Course
    key={course.id}
    id={course.id}
    number={course.number}
    name={course.name}
    campus={course.campus.name}
  />);
}
