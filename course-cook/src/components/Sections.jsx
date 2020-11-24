import React from "react";
import { useQuery } from "urql";

import Section from "./Section";

export default function Sections({ courseId }) {
  const [res] = useQuery({
    query: `
      query Course($courseId: Int!) {
        course_by_pk(id: $courseId) {
          sections {
            id
            crn
            meta
            primary_instructor {
              name
            }
            secondary_instructor {
              name
            }
            slots {
              id
              begin
              building {
                letter
              }
              room {
                number
              }
              days_of_week
              end
              meta
            }
          }
        }
      }
    `,
    variables: { courseId },
  });

  if (res.fetching) return <p>Loading...</p>;
  if (res.error) return <p>Errored!</p>;

  return res.data.course_by_pk.sections.map((section) => <Section
    key={section.id}
    crn={section.crn}
    primary={section.primary_instructor?.name}
    secondary={section.secondary_instructor?.name}
    meta={section.meta}
    slots={section.slots}
  />);
}
