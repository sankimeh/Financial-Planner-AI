import React from "react";
import { Box, Button, IconButton, Paper, TextField, Typography } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import styled from "@emotion/styled";

const Section = styled(Paper)`
  padding: 16px;
  margin-bottom: 24px;
`;

type Props = {
  insurances: string[];
  onAdd: () => void;
  onRemove: (index: number) => void;
  onChange: (index: number, value: string) => void;
};

const InsuranceSection: React.FC<Props> = ({ insurances, onAdd, onRemove, onChange }) => (
  <Section elevation={3}>
    <Typography variant="h6" mb={2}>Insurances</Typography>
    {insurances.map((insurance, index) => (
      <Box key={index} display="flex" alignItems="center" mb={1} gap={1}>
        <TextField
          label={`Insurance ${index + 1}`}
          value={insurance}
          onChange={(e) => onChange(index, e.target.value)}
          fullWidth
        />
        <IconButton onClick={() => onRemove(index)}><DeleteIcon /></IconButton>
      </Box>
    ))}
    <Button onClick={onAdd}>Add Insurance</Button>
  </Section>
);

export default InsuranceSection;
