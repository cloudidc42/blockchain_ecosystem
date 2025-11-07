/**
 * TypeScript type definitions for Blockchain Explorer
 */

export interface Block {
  number: number;
  hash: string;
  parentHash: string;
  timestamp: number;
  miner: string;
  difficulty: number;
  totalDifficulty: number;
  size: number;
  gasLimit: number;
  gasUsed: number;
  transactionCount: number;
  nonce?: string;
  extraData?: string;
  transactions?: string[];
  baseFeePerGas?: number;
}

export interface BlockList {
  blocks: Block[];
  total: number;
  page: number;
  page_size: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface Transaction {
  hash: string;
  blockNumber: number;
  from: string;
  to: string | null;
  value: string;
  gas: number;
  gasPrice: number;
  nonce: number;
  transactionIndex: number;
  input?: string;
  blockHash?: string;
}

export interface TransactionReceipt {
  transactionHash: string;
  blockNumber: number;
  blockHash: string;
  from: string;
  to: string | null;
  gasUsed: number;
  cumulativeGasUsed: number;
  effectiveGasPrice?: number;
  status: number;
  logs: any[];
  contractAddress: string | null;
}

export interface Address {
  address: string;
  balance: string;
  balance_eth: number;
  transaction_count: number;
  is_contract: boolean;
}

export interface BlockchainStats {
  latest_block: number;
  total_transactions: number;
  avg_block_time: number;
  avg_gas_price: number;
  difficulty: number;
  pending_transactions: number;
}

export interface GasStats {
  slow: number;
  standard: number;
  fast: number;
  instant: number;
  base_fee: number | null;
}

export interface HealthCheck {
  status: string;
  version: string;
  connected: boolean;
  latest_block: number | null;
  chain_id: number | null;
}
