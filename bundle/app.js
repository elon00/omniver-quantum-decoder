import { AnnaAppRuntime } from "/static/anna-apps/_sdk/latest/index.js";

const EXECUTA_HANDLE = "omniver-quantum-decoder";
const DEV_FALLBACK_TOOL_ID = "tool-dev-omniver-quantum-decoder";
const TOOL_ID = window.__ANNA_TOOL_IDS__?.[EXECUTA_HANDLE] || DEV_FALLBACK_TOOL_ID;
const $ = (id) => document.getElementById(id);

let anna;
const ready = (async () => {
  try {
    anna = await AnnaAppRuntime.connect();
    $("runtime-status").textContent = "Anna Runtime: connected";
    $("runtime-detail").textContent = "Connected";
    $("tool-status").textContent = TOOL_ID === DEV_FALLBACK_TOOL_ID ? "Local fallback" : "Platform tool";
  } catch (error) {
    $("runtime-status").textContent = "Anna Runtime: unavailable";
    $("runtime-detail").textContent = "Not connected — run inside Anna";
    $("tool-status").textContent = "Runtime error";
    throw error;
  }
  return anna;
})();

async function invoke(method, args) {
  const host = await ready;
  return host.tools.invoke({ tool_id: TOOL_ID, method, args });
}

$("factor").addEventListener("click", async () => {
  const n = Number($("number").value);
  const rawBase = $("base").value.trim();
  const args = { n };
  if (rawBase) args.a = Number(rawBase);
  $("factor").disabled = true;
  $("factor-output").textContent = "Running Shor-style order finding…";
  try {
    const result = await invoke("shor_factor", args);
    $("factor-output").textContent = JSON.stringify(result?.data ?? result, null, 2);
    const data = result?.data ?? result;
    if (data?.factors?.length) {
      $("prompt").value = `Explain the quantum-security significance of factoring N=${n} with factors ${data.factors.join(" × ")}. Distinguish simulator output from a real quantum attack.`;
    }
  } catch (error) {
    $("factor-output").textContent = `Decode failed: ${error?.message || String(error)}`;
  } finally {
    $("factor").disabled = false;
  }
});

$("ask").addEventListener("click", async () => {
  const prompt = $("prompt").value.trim();
  if (!prompt) {
    $("copilot-output").textContent = "Enter a question first.";
    return;
  }
  $("ask").disabled = true;
  $("copilot-output").textContent = "Asking Anna host LLM through reverse sampling…";
  try {
    const result = await invoke("quantum_copilot", { prompt, max_tokens: 512 });
    const data = result?.data ?? result;
    $("copilot-output").textContent = data?.text || JSON.stringify(data, null, 2);
  } catch (error) {
    const message = error?.message || String(error);
    $("copilot-output").textContent = `Copilot failed: ${message}\n\nIf this says SAMPLING_NOT_GRANTED, enable the Executa sampling grant in Anna Admin and retry.`;
  } finally {
    $("ask").disabled = false;
  }
});

ready.catch(() => {});
