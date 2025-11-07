/**
 * Utility Functions for Formatting Data
 */

/**
 * Format address - show first 6 and last 4 characters
 */
export function formatAddress(address: string, startChars: number = 6, endChars: number = 4): string {
  if (!address) return '';
  if (address.length < startChars + endChars) return address;
  return `${address.slice(0, startChars)}...${address.slice(-endChars)}`;
}

/**
 * Format hash - show first 10 and last 8 characters
 */
export function formatHash(hash: string, startChars: number = 10, endChars: number = 8): string {
  if (!hash) return '';
  if (hash.length < startChars + endChars) return hash;
  return `${hash.slice(0, startChars)}...${hash.slice(-endChars)}`;
}

/**
 * Format number with thousand separators
 */
export function formatNumber(num: number | string): string {
  const n = typeof num === 'string' ? parseFloat(num) : num;
  if (isNaN(n)) return '0';
  return n.toLocaleString('en-US');
}

/**
 * Format Wei to Ether
 */
export function formatWei(wei: string | number, decimals: number = 4): string {
  const weiNum = typeof wei === 'string' ? BigInt(wei) : BigInt(wei);
  const ether = Number(weiNum) / 1e18;
  return ether.toFixed(decimals);
}

/**
 * Format Gwei
 */
export function formatGwei(wei: string | number): string {
  const weiNum = typeof wei === 'string' ? BigInt(wei) : BigInt(wei);
  const gwei = Number(weiNum) / 1e9;
  return gwei.toFixed(2);
}

/**
 * Format timestamp to date string
 */
export function formatTimestamp(timestamp: number): string {
  return new Date(timestamp * 1000).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
}

/**
 * Format time ago (e.g., "2 hours ago")
 */
export function formatTimeAgo(timestamp: number): string {
  const now = Math.floor(Date.now() / 1000);
  const diff = now - timestamp;

  if (diff < 60) return `${diff} secs ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)} mins ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} hours ago`;
  if (diff < 2592000) return `${Math.floor(diff / 86400)} days ago`;
  if (diff < 31536000) return `${Math.floor(diff / 2592000)} months ago`;
  return `${Math.floor(diff / 31536000)} years ago`;
}

/**
 * Format bytes to human readable
 */
export function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
}

/**
 * Format gas usage percentage
 */
export function formatGasUsagePercent(gasUsed: number, gasLimit: number): string {
  const percent = (gasUsed / gasLimit) * 100;
  return percent.toFixed(2);
}

/**
 * Copy to clipboard
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (err) {
    console.error('Failed to copy:', err);
    return false;
  }
}

/**
 * Parse hex string to number
 */
export function hexToNumber(hex: string): number {
  return parseInt(hex, 16);
}

/**
 * Parse hex string to BigInt
 */
export function hexToBigInt(hex: string): bigint {
  return BigInt(hex);
}

/**
 * Get transaction status label
 */
export function getStatusLabel(status: number): string {
  switch (status) {
    case 1:
      return 'Success';
    case 0:
      return 'Failed';
    default:
      return 'Pending';
  }
}

/**
 * Get transaction type label
 */
export function getTransactionType(tx: { to: string | null; input: string }): string {
  if (!tx.to) return 'Contract Creation';
  if (tx.input && tx.input !== '0x') return 'Contract Interaction';
  return 'Transfer';
}
