import React, {useState} from 'react';
import {useQuery} from 'graphql-hooks'
import {
  CircularProgress,
  Select,
  InputLabel,
  FormControl
} from '@material-ui/core';
import {
  Alert,
} from '@material-ui/lab';
import {makeStyles} from '@material-ui/core/styles';

const useStyles = makeStyles(theme => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
}));

const SEMESTER_QUERY = `query {
  allSemesters(orderBy: ID_DESC) {
    nodes {
      id
      year
      term
      level
    }
  }
}`;

export default function Semesters() {
  const classes = useStyles();
  const {loading, error, data} = useQuery(SEMESTER_QUERY);
  const [semesterId, setSemesterId] = useState('');

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">Someting went wrong!</Alert>

  const nodes = data.allSemesters.nodes;

  const handleChange = (event) => {
    setSemesterId(event.target.value);
  };

  return (
    <FormControl className={classes.formControl}>
      <InputLabel id="Semester-select-label">Semester</InputLabel>
      <Select
        native
        labelId="Semester-select-label"
        value={semesterId}
        onChange={handleChange}
      >
        <option value="" />
        {nodes.map(({id, year, term, level}) => (
          <option
            key={id}
            value={id}
          >
            {`${year}-${year+1} ${term === 1 ? 'Fall' : 'Winter'} (${level === 1 ? 'Undergrad' : 'Graduate'})`}
          </option>
        ))}
      </Select>
    </FormControl>
  )
}
