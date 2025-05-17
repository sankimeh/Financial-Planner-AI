import React from "react";
import {
  Paper,
  Typography,
  FormGroup,
  FormControlLabel,
  Checkbox,
} from "@mui/material";
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

const commonInsuranceOptions = [
  "Health Insurance",
  "Life Insurance",
  "Auto Insurance",
  "Homeowners/Renters Insurance",
  "Disability Insurance",
  "Long-term Care Insurance",
  "Travel Insurance",
  "Pet Insurance",
];

const InsuranceSection: React.FC<Props> = ({
  insurances,
  onAdd,
  onRemove,
  onChange,
}) => {
  const handleToggle = (insuranceType: string) => {
    const index = insurances.indexOf(insuranceType);
    if (index !== -1) {
      onRemove(index);
    } else {
      onAdd();
      onChange(insurances.length, insuranceType);
    }
  };

  return (
    <Section elevation={3}>
      <Typography variant="h6" mb={2}>
        Insurances
      </Typography>
      <FormGroup>
        {commonInsuranceOptions.map((option) => (
          <FormControlLabel
            key={option}
            control={
              <Checkbox
                checked={insurances.includes(option)}
                onChange={() => handleToggle(option)}
              />
            }
            label={option}
          />
        ))}
      </FormGroup>
    </Section>
  );
};

export default InsuranceSection;
