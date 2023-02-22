import { LineItem } from '.'

export interface InvoiceList {
  consInvNumber?: string
  invoiceNumber: string
  invoices: Invoice[],
  paymentMethod: string
  paymentSystem: string
  statusCode: string
  invoiceAmount: number
  paidAmount: number
}

export interface Invoice {
  bcolAccount: string
  businessIdentifier: string
  corpTypeCode: string
  createdBy: string
  createdName: string
  paymentDate: string
  id: number
  lineItems: LineItem[]
  paid: number
  paidOn: string
  paymentMethod: string
  refund: number
  refundDate: string
  serviceFees: number
  statusCode: string
  total: number
  isOnlineBankingAllowed?: boolean
}

export interface InvoiceListResponse {
  items: InvoiceList[]
  limit: number
  page: number
  total: number
}

export interface FailedInvoice {
  nsfCount?: number
  nsfFee?:number
  totalTransactionAmount?: number
  totalAmountToPay?: number
}
