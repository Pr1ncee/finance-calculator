import FetchHttpClient from '@/api/FetchHttpClient'
import { ApiResponse } from '@/domain/api/apiResponse'
import { RatesInput } from '@/domain/entities/ratesInput'
import LoanMapper from '@/domain/mappers/loanMapper'
import { Loan } from '@/domain/entities/loan'
import { SortBy } from '@/domain/enums/sortBy'
import { OrderBy } from '@/domain/enums/orderBy'

export default class FinanceCalculatorApi {
  private httpClient: FetchHttpClient
  private API_URL = 'http://localhost:8000'
  private loanMapper: LoanMapper

  public constructor(httpClient: FetchHttpClient) {
    this.httpClient = httpClient
    this.loanMapper = new LoanMapper()
  }
  async generateRates(data: RatesInput): Promise<ApiResponse> {
    const loanData = this.loanMapper.mapLoanInput(data)
    return await this.httpClient.makeApiRequest(
      `${this.API_URL}/api/v1/loans/`,
      'POST',
      JSON.stringify(loanData)
    )
  }
  async getLoans(sortBy?: SortBy, orderBy?: OrderBy): Promise<Loan[]> {
    const params = sortBy ? `?sort_by=${sortBy}` + (orderBy ? `&order_by=${orderBy}` : '') : ''

    const result = await this.httpClient.makeApiRequest(
      `${this.API_URL}/api/v1/loans/${params}`,
      'GET',
      null
    )
    return this.loanMapper.mapLoansResponse(result)
  }
}
