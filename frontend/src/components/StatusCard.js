import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import useStyles from '../styles';

const StatusCard = ({ title, count, color }) => {
  const classes = useStyles();

  return (
    <Card className={classes.card} style={{ borderLeft: `5px solid ${color}` }}>
      <CardContent>
        <Typography variant="h6">{title}</Typography>
        <Typography variant="h4">{count}</Typography>
      </CardContent>
    </Card>
  );
};

export default StatusCard;
