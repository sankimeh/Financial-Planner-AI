export interface Allocation {
  equity: number;
  bonds: number;
  commodities: number;
}

export interface GoalAnalysis {
  monthly_surplus: number;
  emergency_fund_ok: boolean;
  ideal_emergency_fund: number;
  recommended_allocation: Allocation;
}

export interface PickItem {
  ticker: string;
  name: string;
  horizon: string;
  reason: string;
}

export interface LLMPicks {
  summary: string;
  equity_picks?: PickItem[];
  bond_picks?: PickItem[];
  commodity_picks?: PickItem[];
}
