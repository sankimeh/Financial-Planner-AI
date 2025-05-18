import React from 'react';
import { Typography, Card, CardContent, CircularProgress, Box } from '@mui/material';

interface Props {
  goals: string[];
  loading: boolean;
}

const SuggestedGoals: React.FC<Props> = ({ goals, loading }) => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6">Suggested Goals</Typography>
        {loading ? (
          <Box display="flex" justifyContent="center" alignItems="center" p={4}>
            <CircularProgress />
          </Box>
        ) : (
          <ul>
            {goals.map((goal, i) => (
              <li key={i}>{goal}</li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
};

export default SuggestedGoals;
