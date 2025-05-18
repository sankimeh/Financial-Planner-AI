import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

interface Props {
  suggestedGoals: string[];
  loading: boolean;
  renderLoader: () => JSX.Element;
}

const GoalSuggestions: React.FC<Props> = ({ suggestedGoals, loading, renderLoader }) => (
  <Card>
    <CardContent>
      <Typography variant="h6">Suggested Goals</Typography>
      {loading ? renderLoader() : (
        <ul>
          {suggestedGoals.map((goal, i) => (
            <li key={i}>{goal}</li>
          ))}
        </ul>
      )}
    </CardContent>
  </Card>
);

export default GoalSuggestions;
