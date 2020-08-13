import React from 'react';
import {Select} from 'grommet';
import {useQuery} from 'graphql-hooks'

const SUBJECTS_QUERY = `query {
  allSubjects {
    nodes {
      id
      name
    }
  }
}`;

const converter = (data) => {
  const nodes = data.allSubjects.nodes;
  return nodes;
};

export default function Subjects({subjectIds, setSubjectIds}) {
  const {loading, error, data} = useQuery(SUBJECTS_QUERY);

  if (loading) return <p>loading</p>
  if (error) return <p>Someting went wrong loading subjects!</p>

  const options = converter(data);

  return <Select
    size="medium"
    multiple
    closeOnChange={false}
    value={subjectIds ?? []}
    valueKey={{key: 'id', reduce: true}}
    options={options}
    labelKey="name"
    onChange={({value}) => {
      if (value.length === 0) {
        setSubjectIds(null);
      }

      setSubjectIds(value);
    }}
  />
}
