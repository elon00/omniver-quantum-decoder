import { SolanaPlayerProfile, SolanaTransactionRecord } from "../types";
import { sha256 } from "@noble/hashes/sha256.js";
import { bytesToHex, hexToBytes } from "../lib/pqcCrypto";

const LOCAL_STORAGE_KEY_PLAYER = "omniver_solana_player_profile_v1";
const LOCAL_STORAGE_KEY_TXS = "omniver_solana_transactions_v1";

// Base58 alphabet for Solana addresses
const ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";

function encodeBase58(bytes: Uint8Array): string {
  const digits = [0];
  for (let i = 0; i < bytes.length; i++) {
    for (let j = 0; j < digits.length; j++) digits[j] <<= 8;
    digits[0] += bytes[i];
    let carry = 0;
    for (let j = 0; j < digits.length; ++j) {
      digits[j] += carry;
      carry = (digits[j] / 58) | 0;
      digits[j] %= 58;
    }
    while (carry) {
      digits.push(carry % 58);
      carry = (carry / 58) | 0;
    }
  }
  for (let i = 0; i < bytes.length && bytes[i] === 0; i++) digits.push(0);
  return digits.reverse().map((digit) => ALPHABET[digit]).join("");
}

export function generateCryptoSolanaPubkey(seedStr: string = "omniver-genesis-key"): string {
  const seedBytes = new TextEncoder().encode(seedStr + Date.now().toString());
  const hash = sha256(seedBytes);
  return encodeBase58(hash).substring(0, 44);
}

export function generateCryptoSignature(payload: string): string {
  const hash1 = sha256(new TextEncoder().encode(payload));
  const hash2 = sha256(new Uint8Array([...hash1, ...new TextEncoder().encode("solana-signature-sig")]));
  const fullBytes = new Uint8Array(64);
  fullBytes.set(hash1, 0);
  fullBytes.set(hash2, 32);
  return encodeBase58(fullBytes);
}

export function getInitialPlayerProfile(): SolanaPlayerProfile {
  try {
    const saved = localStorage.getItem(LOCAL_STORAGE_KEY_PLAYER);
    if (saved) {
      return JSON.parse(saved);
    }
  } catch (e) {
    // fallback
  }

  const initial: SolanaPlayerProfile = {
    publicKey: generateCryptoSolanaPubkey("omniver-pqc-init"),
    balanceSol: 4.82,
    qBitsTokens: 150,
    level: 1,
    experience: 80,
    tasksCompleted: 1,
    badges: [
      {
        id: "badge_novice",
        title: "Qubit Initiate",
        description: "Registered on-chain PDA and initialized quantum execution pipeline",
        unlockedAt: new Date(Date.now() - 3600000).toISOString(),
        icon: "zap",
      },
    ],
  };

  savePlayerProfile(initial);
  return initial;
}

export function savePlayerProfile(profile: SolanaPlayerProfile) {
  try {
    localStorage.setItem(LOCAL_STORAGE_KEY_PLAYER, JSON.stringify(profile));
  } catch (e) {
    console.error("Failed to save player profile", e);
  }
}

export function getInitialTransactions(playerPubkey: string): SolanaTransactionRecord[] {
  try {
    const saved = localStorage.getItem(LOCAL_STORAGE_KEY_TXS);
    if (saved) {
      return JSON.parse(saved);
    }
  } catch (e) {
    // fallback
  }

  const sig = generateCryptoSignature(`genesis_init_001:${playerPubkey}`);
  const initial: SolanaTransactionRecord[] = [
    {
      signature: sig,
      slot: 284109201,
      blockTime: new Date(Date.now() - 1000 * 60 * 25).toISOString(),
      instruction: "initialize_player",
      player: playerPubkey,
      points: 50,
      taskId: "genesis_init_001",
      status: "finalized",
      explorerUrl: `https://explorer.solana.com/tx/${sig}?cluster=devnet`,
    },
  ];

  saveTransactions(initial);
  return initial;
}

export function saveTransactions(txs: SolanaTransactionRecord[]) {
  try {
    localStorage.setItem(LOCAL_STORAGE_KEY_TXS, JSON.stringify(txs));
  } catch (e) {
    console.error("Failed to save transactions", e);
  }
}

export function recordOnChainDecodeProof(
  player: SolanaPlayerProfile,
  pointsEarned: number,
  taskId: string,
  badgeTitle?: string
): { updatedProfile: SolanaPlayerProfile; newTx: SolanaTransactionRecord } {
  const payload = `${player.publicKey}:${pointsEarned}:${taskId}:${Date.now()}`;
  const signature = generateCryptoSignature(payload);
  const slot = 284110000 + (parseInt(bytesToHex(sha256(new TextEncoder().encode(payload))).slice(0, 4), 16) % 50000);

  const updatedExp = player.experience + pointsEarned;
  const newLevel = Math.floor(updatedExp / 100) + 1;
  const updatedTokens = player.qBitsTokens + pointsEarned * 2;
  const updatedTasks = player.tasksCompleted + 1;

  const updatedBadges = [...player.badges];
  if (badgeTitle && !updatedBadges.some((b) => b.title === badgeTitle)) {
    const badgeId = "badge_" + bytesToHex(sha256(new TextEncoder().encode(badgeTitle))).substring(0, 8);
    updatedBadges.push({
      id: badgeId,
      title: badgeTitle,
      description: `Awarded for solving task #${taskId} with quantum precision.`,
      unlockedAt: new Date().toISOString(),
      icon: "award",
    });
  }

  const updatedProfile: SolanaPlayerProfile = {
    ...player,
    experience: updatedExp,
    level: newLevel,
    qBitsTokens: updatedTokens,
    tasksCompleted: updatedTasks,
    badges: updatedBadges,
  };

  const newTx: SolanaTransactionRecord = {
    signature,
    slot,
    blockTime: new Date().toISOString(),
    instruction: badgeTitle ? "mint_badge" : "update_score",
    player: player.publicKey,
    points: pointsEarned,
    taskId,
    status: "finalized",
    explorerUrl: `https://explorer.solana.com/tx/${signature}?cluster=devnet`,
  };

  savePlayerProfile(updatedProfile);

  const currentTxs = getInitialTransactions(player.publicKey);
  const updatedTxs = [newTx, ...currentTxs];
  saveTransactions(updatedTxs);

  return { updatedProfile, newTx };
}
