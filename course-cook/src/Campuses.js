import React from 'react';
import {useQuery} from 'graphql-hooks'
import {
  CircularProgress,
  Select,
  InputLabel,
  FormControl,
  MenuItem,
  Checkbox,
  ListItemText,
  Button,
  Box,
} from '@material-ui/core';
import {
  Alert,
} from '@material-ui/lab';
import {makeStyles} from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  formControl: {
    marginTop: theme.spacing(3),
    width: '100%',
  },
}));

const CAMPUS_QUERY = `query {
  allCampuses {
    nodes {
      name
      id
    }
  }
}`;

export default function Campuses({campusIds, setCampusIds}) {
  const classes = useStyles();
  const {loading, error, data} = useQuery(CAMPUS_QUERY);

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">Someting went wrong loading campuses!</Alert>

  const nodes = data.allCampuses.nodes;

  const handleSelectAll = () => setCampusIds(nodes.map((campus) => campus.id));
  const handleClear = () => setCampusIds([]);

  const handleChange = (event) => setCampusIds(event.target.value);
  const renderValue = (selected) => selected.map((id) => nodes.find(({id: campusId}) => campusId === id).name).join(', ');

  return (
    <FormControl className={classes.formControl}>
      <InputLabel id="Campuses-select-label">Campuses</InputLabel>
      <Select
        multiple
        labelId="Campuses-select-label"
        renderValue={renderValue}
        value={campusIds}
        onChange={handleChange}
      >
        {nodes.map(({id, name}) => (
          <MenuItem
            key={id}
            value={id}
          >
            <Checkbox checked={campusIds.indexOf(id) > -1} />
            <ListItemText primary={name} />
          </MenuItem>
        ))}
      </Select>
      <Box paddingTop={1}>
        <Button
          variant="contained"
          onClick={handleSelectAll}
        >
          Select all
        </Button>
        <Button
          variant="contained"
          onClick={handleClear}
        >
          Clear
        </Button>
      </Box>
    </FormControl>
  )
}
