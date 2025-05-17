import React from "react";
import {
  Box,
  Button,
  IconButton,
  Paper,
  Select,
  MenuItem,
  Typography,
  TextField,
  FormControl,
  InputLabel,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import styled from "@emotion/styled";

const Section = styled(Paper)`
  padding: 24px;
  margin-bottom: 24px;
`;

type Loan = {
  type: string;
  amount: string;
  tenure_months: string;
  installment: string;
  interest_rate: string;
};

type Props = {
  loans: Loan[];
  onAdd: () => void;
  onRemove: (index: number) => void;
  onChange: (index: number, field: keyof Loan, value: string) => void;
};

const loanTypes = [
  "Home Loan",
  "Auto Loan",
  "Student Loan",
  "Personal Loan",
  "Credit Card",
  "Other",
];

const LoanSection: React.FC<Props> = ({ loans, onAdd, onRemove, onChange }) => (
  <Section elevation={3}>
    <Typography variant="h6" gutterBottom>
      Loans
    </Typography>

    {loans.map((loan, index) => (
      <Box key={index} mb={4}>
        {/* First row */}
        <Box display="flex" gap={2} flexWrap="wrap" alignItems="center" mb={1}>
          <FormControl
            sx={{ flexGrow: 1, flexBasis: "140px", minWidth: "140px" }}
            size="small"
          >
            <InputLabel id={`loan-type-label-${index}`}>Type</InputLabel>
            <Select
              labelId={`loan-type-label-${index}`}
              value={loan.type}
              label="Type"
              onChange={(e) => onChange(index, "type", e.target.value)}
            >
              {loanTypes.map((type) => (
                <MenuItem key={type} value={type}>
                  {type}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <TextField
            label="Amount"
            value={loan.amount}
            onChange={(e) => onChange(index, "amount", e.target.value)}
            type="number"
            size="small"
            sx={{ flexGrow: 1, flexBasis: "140px", minWidth: "140px" }}
          />

          <TextField
            label="Tenure (months)"
            value={loan.tenure_months}
            onChange={(e) => onChange(index, "tenure_months", e.target.value)}
            type="number"
            size="small"
            sx={{ flexGrow: 1, flexBasis: "140px", minWidth: "140px" }}
          />
        </Box>

        {/* Second row */}
        <Box display="flex" gap={2} flexWrap="wrap" alignItems="flex-start">
          <TextField
            label="Installment"
            value={loan.installment}
            onChange={(e) => onChange(index, "installment", e.target.value)}
            type="number"
            size="small"
            sx={{ flexGrow: 1, flexBasis: "140px", minWidth: "140px" }}
          />

          <TextField
            label="Interest Rate (%)"
            value={loan.interest_rate}
            onChange={(e) => onChange(index, "interest_rate", e.target.value)}
            type="number"
            size="small"
            sx={{ flexGrow: 1, flexBasis: "140px", minWidth: "140px" }}
          />

          <IconButton
            onClick={() => onRemove(index)}
            aria-label="remove loan"
            sx={{ alignSelf: "flex-start", mt: 1 }}
          >
            <DeleteIcon />
          </IconButton>
        </Box>
      </Box>
    ))}

    <Button onClick={onAdd} variant="outlined" size="small">
      Add Loan
    </Button>
  </Section>
);

export default LoanSection;
