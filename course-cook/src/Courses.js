import React from 'react';
import {useQuery} from 'graphql-hooks'
import {
  Box,
  Paper,
  Typography,
  CircularProgress,
} from '@material-ui/core';
import {
  Alert,
} from '@material-ui/lab';
import {makeStyles} from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(3),
  },
}));

const COURSES_QUERY = `query($semesterId : Int, $campusIds : [Int!]) {
  allCourses(
    filter: {
      semesterId: {equalTo: $semesterId}
      campusId: {in: $campusIds}
    }
  ) {
    nodes {
      id
      subject
      number
      name
    }
  }
}`;

export default function Courses({semesterId, campusIds}) {
  const classes = useStyles();
  const {loading, error, data} = useQuery(COURSES_QUERY, {variables: {semesterId, campusIds}});

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">Someting went wrong loading courses!</Alert>

  const nodes = data.allCourses.nodes;

  return (
    <Paper className={classes.paper}>
      <Box p={3}>
        {nodes.map(({id, subject, number, name}) => (
          <Typography key={id}>{`${id} - ${subject} ${number} ${name}`}</Typography>
        ))}
      </Box>
    </Paper>
  )
}
