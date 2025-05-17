import React from "react";
import {
  Box,
  Button,
  IconButton,
  Paper,
  TextField,
  Typography,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import styled from "@emotion/styled";

const Section = styled(Paper)`
  padding: 24px;
  margin-bottom: 24px;
`;

type Goal = {
  name: string;
  target_amount: string;
  months_to_achieve: string;
  current_savings: string;
  sip: string;
  priority: string;
};

type Props = {
  goals: Goal[];
  onAdd: () => void;
  onRemove: (index: number) => void;
  onChange: (index: number, field: keyof Goal, value: string) => void;
};

const GoalSection: React.FC<Props> = ({ goals, onAdd, onRemove, onChange }) => (
  <Section elevation={3}>
    <Typography variant="h6" gutterBottom>
      Goals
    </Typography>

    {goals.map((goal, index) => (
      <Box key={index} mb={4}>
        {/* First row: name, target amount, months to achieve */}
        <Box
          display="flex"
          gap={2}
          flexWrap="wrap"
          alignItems="center"
          mb={1}
        >
          <TextField
            label="Goal Name"
            value={goal.name}
            onChange={(e) => onChange(index, "name", e.target.value)}
            size="small"
            sx={{ flexGrow: 1, flexBasis: "200px", minWidth: "180px" }}
          />
          <TextField
            label="Target Amount"
            value={goal.target_amount}
            onChange={(e) => onChange(index, "target_amount", e.target.value)}
            size="small"
            type="number"
            sx={{ flexGrow: 1, flexBasis: "140px", minWidth: "140px" }}
          />
          <TextField
            label="Months to Achieve"
            value={goal.months_to_achieve}
            onChange={(e) => onChange(index, "months_to_achieve", e.target.value)}
            size="small"
            type="number"
            sx={{ flexGrow: 1, flexBasis: "140px", minWidth: "140px" }}
          />
        </Box>

        {/* Second row: current savings, sip amount, priority, delete button */}
        <Box
          display="flex"
          gap={2}
          flexWrap="wrap"
          alignItems="center"
        >
          <TextField
            label="Current Savings"
            value={goal.current_savings}
            onChange={(e) => onChange(index, "current_savings", e.target.value)}
            size="small"
            type="number"
            sx={{ flexGrow: 1, flexBasis: "140px", minWidth: "140px" }}
          />
          <TextField
            label="SIP Amount"
            value={goal.sip}
            onChange={(e) => onChange(index, "sip", e.target.value)}
            size="small"
            type="number"
            sx={{ flexGrow: 1, flexBasis: "140px", minWidth: "140px" }}
          />
          <TextField
            label="Priority"
            value={goal.priority}
            onChange={(e) => onChange(index, "priority", e.target.value)}
            size="small"
            sx={{ flexGrow: 1, flexBasis: "100px", minWidth: "100px" }}
          />
          <IconButton
            aria-label="delete goal"
            onClick={() => onRemove(index)}
            sx={{ alignSelf: "flex-start", mt: 1 }}
          >
            <DeleteIcon />
          </IconButton>
        </Box>
      </Box>
    ))}

    <Button onClick={onAdd} variant="outlined" size="small">
      Add Goal
    </Button>
  </Section>
);

export default GoalSection;
