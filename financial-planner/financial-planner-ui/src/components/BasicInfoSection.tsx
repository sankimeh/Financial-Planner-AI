import React from "react";
import {
  Paper,
  TextField,
  Typography,
  MenuItem,
  InputAdornment,
  Box,
} from "@mui/material";
import styled from "@emotion/styled";

const Section = styled(Paper)`
  padding: 24px;
  margin-bottom: 24px;
`;

type Props = {
  name: string;
  age: string;
  income: string;
  expenses: string;
  dependents: string;
  emergency_fund: string;
  risk_profile: string;
  onChange: (field: string, value: string) => void;
};

const riskProfiles = ["Conservative", "Moderate", "Aggressive"];

const BasicInfoSection: React.FC<Props> = ({
  name,
  age,
  income,
  expenses,
  dependents,
  emergency_fund,
  risk_profile,
  onChange,
}) => {
  return (
    <Section elevation={3}>
      <Typography variant="h6" gutterBottom>
        Basic Information
      </Typography>

      <Box display="flex" flexDirection="column" gap={2}>
        <TextField
          label="Full Name"
          value={name}
          onChange={(e) => onChange("name", e.target.value)}
          fullWidth
        />

        <Box display="flex" gap={2}>
          <TextField
            label="Age"
            type="text"
            value={age}
            onChange={(e) => onChange("age", e.target.value)}
            fullWidth
          />
          <TextField
            label="Dependents"
            type="text"
            value={dependents}
            onChange={(e) => onChange("dependents", e.target.value)}
            fullWidth
          />
        </Box>

        <Box display="flex" gap={2}>
          <TextField
            label="Monthly Income"
            type="text"
            value={income}
            onChange={(e) => onChange("income", e.target.value)}
            fullWidth
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">₹</InputAdornment>
              ),
            }}
          />

          <TextField
            label="Monthly Expenses"
            type="text"
            value={expenses}
            onChange={(e) => onChange("expenses", e.target.value)}
            fullWidth
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">₹</InputAdornment>
              ),
            }}
          />
        </Box>

        <Box display="flex" gap={2}>
          <TextField
            label="Current Emergency Fund"
            type="text"
            value={emergency_fund}
            onChange={(e) => onChange("emergency_fund", e.target.value)}
            fullWidth
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">₹</InputAdornment>
              ),
            }}
          />

          <TextField
            select
            label="Risk Profile"
            value={risk_profile}
            onChange={(e) => onChange("risk_profile", e.target.value)}
            fullWidth
          >
            {riskProfiles.map((profile) => (
              <MenuItem key={profile} value={profile}>
                {profile}
              </MenuItem>
            ))}
          </TextField>
        </Box>
      </Box>
    </Section>
  );
};

export default BasicInfoSection;
