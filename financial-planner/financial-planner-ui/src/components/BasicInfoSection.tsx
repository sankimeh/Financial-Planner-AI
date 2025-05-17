import React from "react";
import { Paper, TextField, Typography } from "@mui/material";
import styled from "@emotion/styled";

const Section = styled(Paper)`
  padding: 16px;
  margin-bottom: 24px;
`;

type Props = {
  name: string;
  age: string;
  income: string;
  onChange: (field: string, value: string) => void;
};

const BasicInfoSection: React.FC<Props> = ({ name, age, income, onChange }) => (
  <Section elevation={3}>
    <Typography variant="h6" mb={2}>Basic Information</Typography>
    <TextField label="Name" value={name} onChange={(e) => onChange("name", e.target.value)} fullWidth margin="normal" />
    <TextField label="Age" value={age} onChange={(e) => onChange("age", e.target.value)} fullWidth margin="normal" />
    <TextField label="Income" value={income} onChange={(e) => onChange("income", e.target.value)} fullWidth margin="normal" />
  </Section>
);

export default BasicInfoSection;
