import React, {useState} from 'react';
import debugFactory from 'debug';
import {useQuery} from 'graphql-hooks'
import {Text, Button, Grid, Box, DataTable} from 'grommet';

const debug = debugFactory('coursecook:Courses');

const LIMIT = 50;

const COLUMNS = [
  {
    header: 'Subject',
    property: 'subject',
  },
  {
    header: 'Number',
    property: 'number',
  },
  {
    header: 'Session',
    property: 'session',
  },
  {
    header: 'Name',
    property: 'name',
  },
];

const COURSES_QUERY = `
query(
  $first: Int
  $last: Int
  $after: Cursor
  $before: Cursor
  $filter: CourseFilter
) {
  allCourses(
    first: $first
    last: $last
    after: $after
    before: $before
    filter: $filter
  ) {
    totalCount
    edges {
      node {
        id
        sessionBySessionId {
          name
        }
        subjectBySubjectId {
          name
        }
        number
        name
      }
    }
    pageInfo {
      hasPreviousPage
      startCursor
      hasNextPage
      endCursor
    }
  }
}
`;

const converter = (data) => {
  const results = data.allCourses;
  results.processedData = results.edges.map(({node}) => ({
    id: node.id,
    session: node.sessionBySessionId.name,
    subject: node.subjectBySubjectId.name,
    number: node.number,
    name: node.name,
  }));
  debug('converter results', results);
  return results;
};

export default function Courses({semesterId, campusIds, subjectIds}) {
  const [variables, setVariables] = useState({
    after: null,
    before: null,
    filter: {},
  });

  const baseFilter = {
    semesterId: {equalTo: semesterId},
    campusId: {in: campusIds},
  };

  if (subjectIds !== null) {
    baseFilter.subjectId = {in: subjectIds};
  }

  const queryVariables = {
    first: LIMIT,
    ...variables,
    filter: {
      ...variables.filter,
      ...baseFilter,
    }
  };
  debug('queryVariables', queryVariables);

  const {loading, error, data} = useQuery(COURSES_QUERY, {variables: queryVariables});

  if (loading) return <p>loading</p>
  if (error) return <p>Someting went wrong loading semesters!</p>

  const {processedData, totalCount, pageInfo} = converter(data);

  const {hasNextPage, hasPreviousPage, startCursor, endCursor} = pageInfo;
  debug('pageInfo', pageInfo);

  return (
    <>
      <Grid
        columns={{
          count: 3,
          size: 'auto',
        }}
        gap="small"
        margin="small"
      >
        <Box>
          <Button
            primary
            disabled={!hasPreviousPage}
            label="Previous"
            onClick={() => setVariables({
              ...variables,
              after: null,
              first: null,
              before: startCursor,
              last: LIMIT,
            })}
          />
        </Box>
        <Box align="center">
          <Text>{`Total Courses: ${totalCount}`}</Text>
        </Box>
        <Box>
          <Button
            primary
            disabled={!hasNextPage}
            label="Next"
            onClick={() => setVariables({
              ...variables,
              before: null,
              last: null,
              after: endCursor,
              first: LIMIT,
            })}
          />
        </Box>
      </Grid>
      <DataTable
        columns={COLUMNS}
        data={processedData}
        primaryKey="id"
      />
    </>
  );
}
