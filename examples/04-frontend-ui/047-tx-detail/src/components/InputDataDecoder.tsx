/**
 * Input Data Decoder Component
 * Displays and decodes transaction input data
 */

'use client';

import { useState } from 'react';
import { copyToClipboard, formatBytes } from '@/utils/formatters';

interface InputDataDecoderProps {
  input: string;
  decodedInput?: {
    methodName: string;
    parameters: Array<{
      name: string;
      type: string;
      value: string;
      indexed?: boolean;
    }>;
  };
}

export default function InputDataDecoder({ input, decodedInput }: InputDataDecoderProps) {
  const [showRaw, setShowRaw] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    const success = await copyToClipboard(input);
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const inputSize = input ? new Blob([input]).size : 0;

  if (!input || input === '0x') {
    return (
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">Input Data</h2>
        </div>
        <div className="px-6 py-4">
          <p className="text-sm text-gray-500 italic">No input data</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white shadow rounded-lg overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">Input Data</h2>
          <p className="text-sm text-gray-500 mt-1">Size: {formatBytes(inputSize)}</p>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowRaw(!showRaw)}
            className="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50"
          >
            {showRaw ? 'Show Decoded' : 'Show Raw'}
          </button>
          <button
            onClick={handleCopy}
            className="px-3 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            {copied ? '✓ Copied' : '📋 Copy'}
          </button>
        </div>
      </div>

      <div className="px-6 py-4">
        {!showRaw && decodedInput ? (
          // Decoded View
          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Function</h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <code className="text-sm font-mono text-blue-600">
                  {decodedInput.methodName}
                </code>
              </div>
            </div>

            {decodedInput.parameters && decodedInput.parameters.length > 0 && (
              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-2">Parameters</h3>
                <div className="space-y-3">
                  {decodedInput.parameters.map((param, index) => (
                    <div
                      key={index}
                      className="bg-gray-50 rounded-lg p-4 space-y-1"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-gray-700">
                          {param.name || `param${index}`}
                        </span>
                        <span className="text-xs bg-gray-200 px-2 py-1 rounded font-mono">
                          {param.type}
                        </span>
                      </div>
                      <div className="text-sm text-gray-900 font-mono break-all">
                        {param.value}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ) : (
          // Raw Hex View
          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-2">Raw Input Data</h3>
            <div className="bg-gray-50 rounded-lg p-4">
              {/* Function Selector (first 4 bytes) */}
              {input.length >= 10 && (
                <div className="mb-3">
                  <div className="text-xs text-gray-500 mb-1">Function Selector:</div>
                  <code className="text-sm font-mono text-blue-600 break-all">
                    {input.slice(0, 10)}
                  </code>
                </div>
              )}

              {/* Rest of data */}
              {input.length > 10 && (
                <div>
                  <div className="text-xs text-gray-500 mb-1">Parameters (Hex):</div>
                  <pre className="text-xs font-mono text-gray-900 whitespace-pre-wrap break-all">
                    {input.slice(10)}
                  </pre>
                </div>
              )}

              {/* Full data if short */}
              {input.length <= 10 && (
                <code className="text-sm font-mono text-gray-900 break-all">
                  {input}
                </code>
              )}
            </div>

            {/* UTF-8 Attempt (for data with text) */}
            {input.length > 10 && (
              <div className="mt-4">
                <div className="text-xs text-gray-500 mb-1">
                  UTF-8 Interpretation (if applicable):
                </div>
                <div className="bg-gray-50 rounded-lg p-4">
                  <code className="text-xs font-mono text-gray-600 break-all">
                    {tryDecodeUTF8(input.slice(10))}
                  </code>
                </div>
              </div>
            )}
          </div>
        )}

        {/* No decoded data available */}
        {!showRaw && !decodedInput && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="flex items-start">
              <span className="text-yellow-600 mr-2">⚠️</span>
              <div>
                <p className="text-sm text-yellow-800 font-medium">
                  Unable to decode input data
                </p>
                <p className="text-xs text-yellow-700 mt-1">
                  The contract ABI is not available or the function signature is unknown.
                  Switch to "Show Raw" to view the raw hex data.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

/**
 * Try to decode hex string as UTF-8
 */
function tryDecodeUTF8(hex: string): string {
  try {
    // Remove 0x if present
    const cleanHex = hex.replace(/^0x/, '');

    // Convert hex to bytes
    const bytes = [];
    for (let i = 0; i < cleanHex.length; i += 2) {
      bytes.push(parseInt(cleanHex.substr(i, 2), 16));
    }

    // Try to decode as UTF-8
    const decoder = new TextDecoder('utf-8', { fatal: false });
    const text = decoder.decode(new Uint8Array(bytes));

    // Check if result contains mostly printable characters
    const printable = text.split('').filter(c => {
      const code = c.charCodeAt(0);
      return (code >= 32 && code <= 126) || code === 10 || code === 13;
    }).length;

    if (printable / text.length > 0.5) {
      return text;
    }

    return '(Not valid UTF-8 text)';
  } catch (e) {
    return '(Decode error)';
  }
}
