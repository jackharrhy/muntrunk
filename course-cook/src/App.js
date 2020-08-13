import React, {useState} from 'react';
import {Grommet, Main, Heading, Box} from 'grommet';
import {grommet} from 'grommet/themes';
import {GraphQLClient, ClientContext} from 'graphql-hooks';

import Semesters from './Semesters';
import Campuses from './Campuses';
import Courses from './Courses';
import Subjects from './Subjects';

const client = new GraphQLClient({
  url: process.env.REACT_APP_GRAPHQL_ENDPOINT,
})

export default function App() {
  const [semesterId, setSemesterId] = useState(81);
  const [campusIds, setCampusIds] = useState([1]);
  const [subjectIds, setSubjectIds] = useState(null);

  return (
    <ClientContext.Provider value={client}>
      <Grommet theme={grommet}>
        <Main pad="large">
          <Box fill justify="start">
            <Box align="center">
              <Heading margin={{top: 'none', bottom: '1rem'}}>Course Cook</Heading>
              <Box pad="small">
                <Semesters
                  semesterId={semesterId}
                  setSemesterId={setSemesterId}
                />
              </Box>
              <Box pad="small">
                <Campuses
                  campusIds={campusIds}
                  setCampusIds={setCampusIds}
                />
              </Box>
              <Box pad="small">
                <Subjects
                  subjectIds={subjectIds}
                  setSubjectIds={setSubjectIds}
                />
              </Box>
            </Box>
            {
              semesterId !== '' && campusIds.length > 0 && (
                <Courses
                  semesterId={semesterId}
                  campusIds={campusIds}
                  subjectIds={subjectIds}
                />
              )
            }
          </Box>
        </Main>
      </Grommet>
    </ClientContext.Provider>
  );
}
