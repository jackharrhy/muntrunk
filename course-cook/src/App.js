import React, {useState} from 'react';
import {Grommet, Main, Heading, Box} from 'grommet';
import {grommet} from 'grommet/themes';
import {GraphQLClient, ClientContext} from 'graphql-hooks';

import Semesters from './Semesters';
import Campuses from './Campuses';
import Courses from './Courses';

const client = new GraphQLClient({
  url: process.env.REACT_APP_GRAPHQL_ENDPOINT,
})

export default function App() {
  const [semesterId, setSemesterId] = useState(81);
  const [campusIds, setCampusIds] = useState([1]);

  return (
    <ClientContext.Provider value={client}>
      <Grommet theme={grommet}>
        <Main pad="large">
          <Box fill justify="start">
            <Box align="center">
              <Heading margin={{top: "none"}}>Course Cook</Heading>
              <Semesters
                semesterId={semesterId}
                setSemesterId={setSemesterId}
              />
              <Campuses
                campusIds={campusIds}
                setCampusIds={setCampusIds}
              />
            </Box>
            {
              semesterId !== '' && campusIds.length > 0 && (
                <Courses
                  semesterId={semesterId}
                  campusIds={campusIds}
                />
              )
            }
          </Box>
        </Main>
      </Grommet>
    </ClientContext.Provider>
  );
}
