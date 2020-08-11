import React from 'react';
import {Select} from 'grommet';
import {useQuery} from 'graphql-hooks'

const SEMESTER_QUERY = `
query {
  allSemesters(orderBy: ID_DESC) {
    nodes {
      id
      year
      term
      level
    }
  }
}
`;

const converter = (data) => {
  const nodes = data.allSemesters.nodes;

  return nodes.map((node) => {
    const {year, term, level} = node;
    node.label = `${year}-${year+1} ${term === 1 ? 'Fall' : 'Winter'} (${level === 1 ? 'Undergrad' : 'Graduate'})`;
    return node;
  });
};

export default function Semesters({semesterId, setSemesterId}) {
  const {loading, error, data} = useQuery(SEMESTER_QUERY);

  if (loading) return <p>loading</p>
  if (error) return <p>Someting went wrong loading semesters!</p>

  const options = converter(data);

  return <Select
    size="medium"
    value={semesterId}
    valueKey={{key: 'id', reduce: true}}
    options={options}
    labelKey="label"
    onChange={({value}) => setSemesterId(value)}
  />
}
