import React from "react";
import { Box, Button, IconButton, Paper, TextField, Typography } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import styled from "@emotion/styled";

const Section = styled(Paper)`
  padding: 16px;
  margin-bottom: 24px;
`;

type Goal = {
  name: string;
  targetAmount: string;
  timePeriod: string;
};

type Props = {
  goals: Goal[];
  onAdd: () => void;
  onRemove: (index: number) => void;
  onChange: (index: number, field: string, value: string) => void;
};

const GoalSection: React.FC<Props> = ({ goals, onAdd, onRemove, onChange }) => (
  <Section elevation={3}>
    <Typography variant="h6" mb={2}>Goals</Typography>
    {goals.map((goal, index) => (
      <Box key={index} display="flex" flexDirection="column" gap={1} mb={2}>
        <TextField
          label="Goal Name"
          value={goal.name}
          onChange={(e) => onChange(index, "name", e.target.value)}
          fullWidth
        />
        <TextField
          label="Target Amount"
          value={goal.targetAmount}
          onChange={(e) => onChange(index, "targetAmount", e.target.value)}
          fullWidth
        />
        <TextField
          label="Time Period (months)"
          value={goal.timePeriod}
          onChange={(e) => onChange(index, "timePeriod", e.target.value)}
          fullWidth
        />
        <IconButton onClick={() => onRemove(index)}><DeleteIcon /></IconButton>
      </Box>
    ))}
    <Button onClick={onAdd}>Add Goal</Button>
  </Section>
);

export default GoalSection;
