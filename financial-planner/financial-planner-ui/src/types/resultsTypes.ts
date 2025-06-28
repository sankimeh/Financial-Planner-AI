export interface Allocation {
  equity: number;
  bonds: number;
  commodities: number;
}

export interface GoalFeasibility {
  name: string;
  target: number;
  horizon_months: number;
  expected_return_annual: number;
  projected_value: number;
  feasible: boolean;
  recommendation?: {
    suggested_sip: number;
    extend_by_months: number | null;
  };
}

export interface GoalAnalysis {
  monthly_surplus: number;
  emergency_fund_ok: boolean;
  ideal_emergency_fund: number;
  goal_analysis: GoalFeasibility[];
  recommended_allocation: Allocation;
  allocation_explanation: string;
}

export interface PickItem {
  ticker: string;
  name: string;
  horizon: string;
  reason: string;
}

export interface LLMPicks {
  equity_picks?: PickItem[];
  bond_picks?: PickItem[];
  commodity_picks?: PickItem[];
}
