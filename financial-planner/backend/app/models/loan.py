from pydantic import BaseModel

class Loan(BaseModel):
    amount: float
    tenure_months: int
    installment: float
    interest_rate: float  # Annual interest rate in percentage