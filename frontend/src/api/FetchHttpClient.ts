import { ApiResponse } from '@/domain/api/apiResponse'
import ApiException from '@/core/exceptions/apiExceptions'

export default class FetchHttpClient {
  public async makeApiRequest(
    url: string,
    method: string,
    body: string | null
  ): Promise<ApiResponse> {
    const requestOptions = {
      method,
      body,
      headers: {
        'Content-Type': 'application/json'
      }
    }
    try {
      const response = await fetch(url, requestOptions)
      return {
        status: response.status,
        body: await response.json().catch(() => null)
      }
    } catch (error) {
      throw new ApiException()
    }
  }
}
