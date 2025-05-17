import React from "react";
import { Box, Button, IconButton, Paper, TextField, Typography } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import styled from "@emotion/styled";

const Section = styled(Paper)`
  padding: 16px;
  margin-bottom: 24px;
`;

type Loan = { type: string; amount: string };

type Props = {
  loans: Loan[];
  onAdd: () => void;
  onRemove: (index: number) => void;
  onChange: (index: number, field: string, value: string) => void;
};

const LoanSection: React.FC<Props> = ({ loans, onAdd, onRemove, onChange }) => (
  <Section elevation={3}>
    <Typography variant="h6" mb={2}>Loans</Typography>
    {loans.map((loan, index) => (
      <Box key={index} display="flex" gap={1} mb={1}>
        <TextField
          label="Type"
          value={loan.type}
          onChange={(e) => onChange(index, "type", e.target.value)}
          fullWidth
        />
        <TextField
          label="Amount"
          value={loan.amount}
          onChange={(e) => onChange(index, "amount", e.target.value)}
          fullWidth
        />
        <IconButton onClick={() => onRemove(index)}><DeleteIcon /></IconButton>
      </Box>
    ))}
    <Button onClick={onAdd}>Add Loan</Button>
  </Section>
);

export default LoanSection;
