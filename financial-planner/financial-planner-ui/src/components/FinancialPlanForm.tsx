import React, { useState } from "react";
import { Box, Button, Container, Typography } from "@mui/material";
import BasicInfoSection from "./BasicInfoSection";
import InsuranceSection from "./InsurancesSection";
import LoanSection from "./LoansSection";
import GoalSection from "./GoalsSection";
import { useNavigate } from 'react-router-dom';

type Loan = {
  type: string;
  amount: string;
  tenure_months: string;
  installment: string;
  interest_rate: string;
};

type Goal = {
  name: string;
  target_amount: string;
  months_to_achieve: string;
  current_savings: string;
  sip: string;
  priority: string;
};

const FinancialPlanForm: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    age: "",
    income: "",
    expenses: "",
    dependents: "",
    emergency_fund: "",
    risk_profile: "",
    insurances: [""],
    loans: [
      {
        type: "",
        amount: "",
        tenure_months: "",
        installment: "",
        interest_rate: "",
      },
    ] as Loan[],
    goals: [
      {
        name: "",
        target_amount: "",
        months_to_achieve: "",
        current_savings: "",
        sip: "",
        priority: "",
      },
    ] as Goal[],
  });

  const [submitted, setSubmitted] = useState(false);

  const handleInputChange = (field: string, value: string | number) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleInsuranceChange = (index: number, value: string) => {
    const updated = [...formData.insurances];
    updated[index] = value;
    setFormData((prev) => ({ ...prev, insurances: updated }));
  };

  const addInsurance = () =>
    setFormData((prev) => ({ ...prev, insurances: [...prev.insurances, ""] }));

  const removeInsurance = (index: number) =>
    setFormData((prev) => ({
      ...prev,
      insurances: prev.insurances.filter((_, i) => i !== index),
    }));

  const handleLoanChange = (index: number, field: keyof Loan, value: string) => {
    const updated = [...formData.loans];
    updated[index] = { ...updated[index], [field]: value };
    setFormData((prev) => ({ ...prev, loans: updated }));
  };

  const addLoan = () =>
    setFormData((prev) => ({
      ...prev,
      loans: [
        ...prev.loans,
        { type: "", amount: "", tenure_months: "", installment: "", interest_rate: "" },
      ],
    }));

  const removeLoan = (index: number) =>
    setFormData((prev) => ({
      ...prev,
      loans: prev.loans.filter((_, i) => i !== index),
    }));

  const handleGoalChange = (index: number, field: keyof Goal, value: string) => {
    const updated = [...formData.goals];
    updated[index] = { ...updated[index], [field]: value };
    setFormData((prev) => ({ ...prev, goals: updated }));
  };

  const addGoal = () =>
    setFormData((prev) => ({
      ...prev,
      goals: [...prev.goals, { name: "", target_amount: "", months_to_achieve: "", current_savings: "", sip: "", priority: "" }],
    }));

  const removeGoal = (index: number) =>
    setFormData((prev) => ({
      ...prev,
      goals: prev.goals.filter((_, i) => i !== index),
    }));

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Convert string numbers to numeric types for backend readiness
    const loans = formData.loans.map((loan) => ({
      ...loan,
      amount: parseFloat(loan.amount) || 0,
      tenure_months: parseInt(loan.tenure_months) || 0,
      installment: parseFloat(loan.installment) || 0,
      interest_rate: parseFloat(loan.interest_rate) || 0,
    }));

    const goals = formData.goals.map((goal) => ({
      name: goal.name,
      target_amount: parseFloat(goal.target_amount) || 0,
      months_to_achieve: parseInt(goal.months_to_achieve) || 0,
      current_savings: parseFloat(goal.current_savings) || 0,
      sip: parseFloat(goal.sip) || 0,
      priority: goal.priority,
    }));

    const submitData = {
      ...formData,
      loans,
      goals,
    };

    console.log("Submitted data:", submitData);
    setSubmitted(true);

    navigate('/results', { state: submitData });
  };

  return (
    <Container maxWidth="md" sx={{ pb: 6 }}>
      <Typography variant="h3" gutterBottom mt={4} sx={{ fontWeight: "bold", textAlign: "center" }}>
        💰 Your Fun Financial Planner 💸
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3, textAlign: "center" }}>
        Let's turn those numbers into your money magic! ✨
      </Typography>


      <form onSubmit={handleSubmit}>
        <BasicInfoSection
          name={formData.name}
          age={formData.age}
          income={formData.income}
          expenses={formData.expenses}
          dependents={formData.dependents}
          emergency_fund={formData.emergency_fund}
          risk_profile={formData.risk_profile}
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

        <Box mt={5} textAlign="center">
          <Button variant="contained" color="primary" size="large" type="submit" sx={{ fontWeight: "bold", px: 5 }}>
            🚀 Blast Off! Submit Plan
          </Button>
        </Box>
      </form>
    </Container>
  );
};

export default FinancialPlanForm;
