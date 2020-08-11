import React from 'react';
import {useQuery} from 'graphql-hooks'
import {Text, Box} from 'grommet';

const COURSES_QUERY = `
query($semesterId : Int, $campusIds : [Int!]) {
  allCourses(
    filter: {
      semesterId: {equalTo: $semesterId}
      campusId: {in: $campusIds}
    }
  ) {
    nodes {
      id
      subject
      number
      name
    }
  }
}
`;

export default function Courses({semesterId, campusIds}) {
  const {loading, error, data} = useQuery(COURSES_QUERY, {variables: {semesterId, campusIds}});

  if (loading) return <p>loading</p>
  if (error) return <p>Someting went wrong loading semesters!</p>

  const nodes = data.allCourses.nodes;

  return nodes.map(({id, subject, number, name}) => (
    <Box key={id} margin="small">
      <Text>{`${id} - ${subject} ${number} ${name}`}</Text>
    </Box>
  ));
}
