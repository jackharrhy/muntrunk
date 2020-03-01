import React, {useState} from 'react';
import {GraphQLClient, ClientContext} from 'graphql-hooks';
import Semesters from './Semesters';
import Campuses from './Campuses';
import {Container} from '@material-ui/core';

const client = new GraphQLClient({
  url: '/graphql'
})

export default function App() {
  const [semesterId, setSemesterId] = useState('');
  const [campusIds, setCampusIds] = useState([]);

  return (
    <ClientContext.Provider value={client}>
      <Container maxWidth="sm">
        <Semesters
          semesterId={semesterId}
          setSemesterId={setSemesterId}
        />
        <Campuses
          campusIds={campusIds}
          setCampusIds={setCampusIds}
        />
      </Container>
    </ClientContext.Provider>
  );
}
