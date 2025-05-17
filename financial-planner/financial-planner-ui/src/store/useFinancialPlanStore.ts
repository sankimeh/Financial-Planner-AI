// src/store/useFinancialPlanStore.ts
import { create } from 'zustand';

type Loan = {
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

type FormData = {
  name: string;
  age: string;
  income: string;
  expenses: string;
  dependents: string;
  emergency_fund: string;
  insurances: string[];
  loans: Loan[];
  goals: Goal[];
  risk_profile: string;
};

type FinancialPlanState = {
  formData: FormData;
  setField: (field: keyof FormData, value: any) => void;

  // Insurances
  setInsurance: (index: number, value: string) => void;
  addInsurance: () => void;
  removeInsurance: (index: number) => void;

  // Loans
  setLoanField: (index: number, field: keyof Loan, value: string) => void;
  addLoan: () => void;
  removeLoan: (index: number) => void;

  // Goals
  setGoalField: (index: number, field: keyof Goal, value: string) => void;
  addGoal: () => void;
  removeGoal: (index: number) => void;
};

export const useFinancialPlanStore = create<FinancialPlanState>((set) => ({
  formData: {
    name: "",
    age: "",
    income: "",
    expenses: "",
    dependents: "",
    emergency_fund: "",
    insurances: [""],
    loans: [
      {
        amount: "",
        tenure_months: "",
        installment: "",
        interest_rate: "",
      },
    ],
    goals: [
      {
        name: "",
        target_amount: "",
        months_to_achieve: "",
        current_savings: "",
        sip: "",
        priority: "",
      },
    ],
    risk_profile: "",
  },

  setField: (field, value) =>
    set((state) => ({
      formData: { ...state.formData, [field]: value },
    })),

  setInsurance: (index, value) =>
    set((state) => {
      const insurances = [...state.formData.insurances];
      insurances[index] = value;
      return { formData: { ...state.formData, insurances } };
    }),

  addInsurance: () =>
    set((state) => ({
      formData: {
        ...state.formData,
        insurances: [...state.formData.insurances, ""],
      },
    })),

  removeInsurance: (index) =>
    set((state) => {
      const insurances = state.formData.insurances.filter((_, i) => i !== index);
      return { formData: { ...state.formData, insurances } };
    }),

  setLoanField: (index, field, value) =>
    set((state) => {
      const loans = [...state.formData.loans];
      loans[index] = { ...loans[index], [field]: value };
      return { formData: { ...state.formData, loans } };
    }),

  addLoan: () =>
    set((state) => ({
      formData: {
        ...state.formData,
        loans: [
          ...state.formData.loans,
          { amount: "", tenure_months: "", installment: "", interest_rate: "" },
        ],
      },
    })),

  removeLoan: (index) =>
    set((state) => {
      const loans = state.formData.loans.filter((_, i) => i !== index);
      return { formData: { ...state.formData, loans } };
    }),

  setGoalField: (index, field, value) =>
    set((state) => {
      const goals = [...state.formData.goals];
      goals[index] = { ...goals[index], [field]: value };
      return { formData: { ...state.formData, goals } };
    }),

  addGoal: () =>
    set((state) => ({
      formData: {
        ...state.formData,
        goals: [
          ...state.formData.goals,
          { name: "", target_amount: "", months_to_achieve: "", current_savings: "", sip: "", priority: "" },
        ],
      },
    })),

  removeGoal: (index) =>
    set((state) => {
      const goals = state.formData.goals.filter((_, i) => i !== index);
      return { formData: { ...state.formData, goals } };
    }),
}));
