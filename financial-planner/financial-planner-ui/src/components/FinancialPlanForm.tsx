import React, { useState } from "react";
import { Box, Button, Container, Typography } from "@mui/material";
import BasicInfoSection from "./BasicInfoSection";
import InsuranceSection from "./InsurancesSection";
import LoanSection from "./LoansSection";
import GoalSection from "./GoalsSection";


const FinancialPlanForm: React.FC = () => {
  const [formData, setFormData] = useState({
    name: "",
    age: "",
    income: "",
    insurances: [""],
    loans: [{ type: "", amount: "" }],
    goals: [{ name: "", targetAmount: "", timePeriod: "" }],
  });

  const handleInputChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleInsuranceChange = (index: number, value: string) => {
    const updated = [...formData.insurances];
    updated[index] = value;
    setFormData((prev) => ({ ...prev, insurances: updated }));
  };

  const addInsurance = () => setFormData((prev) => ({ ...prev, insurances: [...prev.insurances, ""] }));
  const removeInsurance = (index: number) =>
    setFormData((prev) => ({
      ...prev,
      insurances: prev.insurances.filter((_, i) => i !== index),
    }));

  const handleLoanChange = (index: number, field: string, value: string) => {
    const updated = [...formData.loans];
    updated[index] = { ...updated[index], [field]: value };
    setFormData((prev) => ({ ...prev, loans: updated }));
  };

  const addLoan = () => setFormData((prev) => ({ ...prev, loans: [...prev.loans, { type: "", amount: "" }] }));
  const removeLoan = (index: number) =>
    setFormData((prev) => ({
      ...prev,
      loans: prev.loans.filter((_, i) => i !== index),
    }));

  const handleGoalChange = (index: number, field: string, value: string) => {
    const updated = [...formData.goals];
    updated[index] = { ...updated[index], [field]: value };
    setFormData((prev) => ({ ...prev, goals: updated }));
  };

  const addGoal = () =>
    setFormData((prev) => ({
      ...prev,
      goals: [...prev.goals, { name: "", targetAmount: "", timePeriod: "" }],
    }));

  const removeGoal = (index: number) =>
    setFormData((prev) => ({
      ...prev,
      goals: prev.goals.filter((_, i) => i !== index),
    }));

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Submitted data:", formData);
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h4" gutterBottom mt={4}>
        Financial Plan Form
      </Typography>
      <form onSubmit={handleSubmit}>
        <BasicInfoSection
          name={formData.name}
          age={formData.age}
          income={formData.income}
          onChange={handleInputChange}
        />

        <InsuranceSection
          insurances={formData.insurances}
          onAdd={addInsurance}
          onRemove={removeInsurance}
          onChange={handleInsuranceChange}
        />

        <LoanSection
          loans={formData.loans}
          onAdd={addLoan}
          onRemove={removeLoan}
          onChange={handleLoanChange}
        />

        <GoalSection
          goals={formData.goals}
          onAdd={addGoal}
          onRemove={removeGoal}
          onChange={handleGoalChange}
        />

        <Box mt={4}>
          <Button variant="contained" color="primary" type="submit">
            Submit Plan
          </Button>
        </Box>
      </form>
    </Container>
  );
};

export default FinancialPlanForm;
