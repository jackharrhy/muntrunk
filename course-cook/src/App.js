import React from 'react';
import {GraphQLClient, ClientContext} from 'graphql-hooks';
import Semesters from './Semesters';
import {Container} from '@material-ui/core';

const client = new GraphQLClient({
  url: '/graphql'
})

export default function App() {
  return (
    <ClientContext.Provider value={client}>
      <Container maxWidth="sm">
        <Semesters />
      </Container>
    </ClientContext.Provider>
  );
}
