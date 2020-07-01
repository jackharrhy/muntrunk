import React, {useState} from 'react';
import {GraphQLClient, ClientContext} from 'graphql-hooks';
import {Container, Typography} from '@material-ui/core';
import Semesters from './Semesters';
import Campuses from './Campuses';
import Courses from './Courses';

const client = new GraphQLClient({
  url: process.env.REACT_APP_GRAPHQL_ENDPOINT,
})

export default function App() {
  const [semesterId, setSemesterId] = useState(79);
  const [campusIds, setCampusIds] = useState([1]);

  return (
    <ClientContext.Provider value={client}>
      <Container maxWidth="sm">
        <Typography>Course Cook</Typography>
        <Semesters
          semesterId={semesterId}
          setSemesterId={setSemesterId}
        />
        <Campuses
          campusIds={campusIds}
          setCampusIds={setCampusIds}
        />
        {
          semesterId !== '' && campusIds.length > 0 ? (
            <Courses
              semesterId={semesterId}
              campusIds={campusIds}
            />
          ) : null
        }
      </Container>
    </ClientContext.Provider>
  );
}
