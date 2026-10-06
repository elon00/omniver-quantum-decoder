import fs from "node:fs";
import path from "node:path";

const ROOTS = ["server.ts", "src", "quantumshield"];
const TEXT_EXT = new Set([".ts",".tsx",".js",".mjs",".cjs",".json",".yml",".yaml"]);
const violations = [];
const forbidden = [
  [/mockCounts/g, "fabricated execution counts"],
  [/Simulated ML-KEM/gi, "simulated cryptography"],
  [/fallback entropy for ECDH/gi, "fake cryptographic fallback"],
  [/status:\s*["']COMPLETED["']/g, "hard-coded external execution completion"],
  [/nvapi-[A-Za-z0-9_-]{20,}/g, "hard-coded NVIDIA credential"]
];
function walk(p) {
  if (!fs.existsSync(p)) return;
  const st=fs.statSync(p);
  if(st.isDirectory()) for(const n of fs.readdirSync(p)) {
    if(["node_modules","dist",".git"].includes(n)) continue;
    walk(path.join(p,n));
  } else if(TEXT_EXT.has(path.extname(p)) || p==="server.ts") {
    const t=fs.readFileSync(p,"utf8");
    for(const [re,label] of forbidden) if(re.test(t)) violations.push({file:p,label});
  }
}
for(const p of ROOTS) walk(p);
if(violations.length){
  console.error("REALITY GUARD FAILED");
  for(const v of violations) console.error(`- ${v.file}: ${v.label}`);
  process.exit(1);
}
console.log("REALITY GUARD PASSED: no prohibited fabricated crypto/QPU evidence or embedded NVIDIA credential detected.");
