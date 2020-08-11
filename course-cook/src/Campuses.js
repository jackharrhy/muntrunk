import React from 'react';
import {Select} from 'grommet';
import {useQuery} from 'graphql-hooks'

const CAMPUS_QUERY = `query {
  allCampuses {
    nodes {
      id
      name
    }
  }
}`;

const converter = (data) => {
  const nodes = data.allCampuses.nodes;
  return nodes;
};

export default function Campuses({campusIds, setCampusIds}) {
  const {loading, error, data} = useQuery(CAMPUS_QUERY);

  if (loading) return <p>loading</p>
  if (error) return <p>Someting went wrong loading semesters!</p>

  const options = converter(data);

  return <Select
    size="medium"
    multiple
    closeOnChange={false}
    value={campusIds}
    valueKey={{key: 'id', reduce: true}}
    options={options}
    labelKey="name"
    onChange={({value}) => setCampusIds(value)}
  />
}
