import { ApiResponse } from '@/domain/api/apiResponse'
import { Loan } from '@/domain/entities/loan'
import { RatesInput } from '@/domain/entities/ratesInput'

export default class LoanMapper {
  mapLoansResponse(response: ApiResponse): Loan[] {
    return response.body.map((item: any) => this.mapLoan(item))
  }
  mapLoan(item: any): Loan {
    const loan: Loan = {
      interestRate: item.interest_rate,
      monthlyPayment: item.monthly_payment,
      mortgageTerm: item.mortgage_term,
      totalAmount: item.total_amount,
      totalOverLoanTerm: item.total_over_loan_term
    }

    for (const key in loan) (loan as any)[key] = parseFloat((loan as any)[key].toFixed(2))

    return loan
  }

  mapLoanInput(loanInputData: RatesInput): any {
    return {
      purchase_price: loanInputData.purchasePrice,
      interest_rate: loanInputData.interestRate,
      dollar_down_payment: loanInputData.dollarDownPayment || null,
      percentage_down_payment: loanInputData.percentageDownPayment || null,
      mortgage_term: loanInputData.mortgageTerm
    }
  }
}
