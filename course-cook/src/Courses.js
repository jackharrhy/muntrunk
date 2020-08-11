import React, {useState} from 'react';
import {useQuery} from 'graphql-hooks'
import {Text, Button, DataTable} from 'grommet';

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
    header: 'Name',
    property: 'name',
  },
];

const COURSES_QUERY = `
query(
  $limit: Int,
  $after: Cursor,
  $before: Cursor,
  $semesterId : Int,
  $campusIds : [Int!]
) {
  allCourses(
    first: $limit,
    after: $after,
    before: $before,
    filter: {
      semesterId: {equalTo: $semesterId}
      campusId: {in: $campusIds}
    }
  ) {
    totalCount
    edges {
      cursor
      node {
        id
        subject
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
  return results;
};

export default function Courses({semesterId, campusIds}) {
  const [cursors, setCursors] = useState({after: null, before: null});
  const {loading, error, data} = useQuery(
    COURSES_QUERY,
    {
      variables: {
        limit: LIMIT,
        after: cursors.after,
        before: cursors.before,
        semesterId,
        campusIds,
      }
    }
  );

  if (loading) return <p>loading</p>
  if (error) return <p>Someting went wrong loading semesters!</p>

  const {
    totalCount,
    edges,
    pageInfo: {hasNextPage, hasPreviousPage, startCursor, endCursor}
  } = converter(data);

  return (
    <>
      <Text>{`Total Courses: ${totalCount}`}</Text>
      { hasPreviousPage && (
        <Button
          primary
          label="Previous"
          onClick={() => setCursors({before: startCursor})}
        />
      )}
      { hasNextPage && (
        <Button
          primary
          label="Next"
          onClick={() => setCursors({after: endCursor})}
        />
      )}
      <DataTable
        columns={COLUMNS}
        data={edges.map((edge) => edge.node)}
        primaryKey="id"
      />
    </>
  );
}
