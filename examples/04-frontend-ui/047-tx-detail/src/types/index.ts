/**
 * Type Definitions for Transaction Detail Page
 */

export interface Transaction {
  hash: string;
  blockNumber: number;
  blockHash: string;
  timestamp: number;
  from: string;
  to: string | null;
  value: string;
  gas: number;
  gasPrice: string;
  gasUsed?: number;
  nonce: number;
  input: string;
  transactionIndex: number;
  status?: number;
  contractAddress?: string | null;
}

export interface TransactionReceipt {
  transactionHash: string;
  transactionIndex: number;
  blockNumber: number;
  blockHash: string;
  from: string;
  to: string | null;
  cumulativeGasUsed: number;
  gasUsed: number;
  contractAddress: string | null;
  logs: TransactionLog[];
  logsBloom: string;
  status: number;
  effectiveGasPrice?: string;
}

export interface TransactionLog {
  address: string;
  topics: string[];
  data: string;
  blockNumber: number;
  transactionHash: string;
  transactionIndex: number;
  blockHash: string;
  logIndex: number;
  removed: boolean;
}

export interface DecodedLog {
  address: string;
  eventName: string;
  parameters: DecodedParameter[];
  logIndex: number;
}

export interface DecodedParameter {
  name: string;
  type: string;
  value: string;
  indexed: boolean;
}

export interface TransactionDetail {
  transaction: Transaction;
  receipt: TransactionReceipt;
  confirmations: number;
  decodedLogs?: DecodedLog[];
  decodedInput?: DecodedInput;
}

export interface DecodedInput {
  methodName: string;
  parameters: DecodedParameter[];
}

export interface InternalTransaction {
  from: string;
  to: string;
  value: string;
  gas: number;
  gasUsed: number;
  type: string;
  traceAddress: number[];
  error?: string;
}

export interface TransactionStats {
  totalFee: string;
  gasPrice: string;
  gasUsed: number;
  gasLimit: number;
  gasSaved: number;
  effectiveGasPrice?: string;
}

// ERC-20 Transfer Event
export interface ERC20Transfer {
  from: string;
  to: string;
  value: string;
  tokenAddress: string;
  tokenSymbol?: string;
  tokenDecimals?: number;
}

// ERC-721 Transfer Event
export interface ERC721Transfer {
  from: string;
  to: string;
  tokenId: string;
  tokenAddress: string;
  tokenName?: string;
}

export interface TokenTransfer {
  type: 'ERC20' | 'ERC721' | 'ERC1155';
  from: string;
  to: string;
  value?: string;
  tokenId?: string;
  tokenAddress: string;
  tokenSymbol?: string;
  tokenName?: string;
}

export enum TransactionStatus {
  SUCCESS = 1,
  FAILED = 0,
  PENDING = -1,
}

export interface Block {
  number: number;
  hash: string;
  timestamp: number;
  miner: string;
  gasUsed: number;
  gasLimit: number;
  transactionCount: number;
}
