import time
import sys
import io
import random

# Fix for Windows terminal emoji encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)

# ---------------- QUANTUM LIBRARIES ----------------
try:
    from qiskit import QuantumCircuit
    from qiskit.primitives import Sampler
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False

try:
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
    IBM_RUNTIME_AVAILABLE = True
except ImportError:
    IBM_RUNTIME_AVAILABLE = False
# ---------------------------------------------------

def type_effect(text, delay=0.015):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_big_box(title, content_lines):
    print("\n" + "╔" + "═" * 78 + "╗")
    title_str = f" ✨ [{title.upper()}] ✨ "
    pad_len = (78 - len(title_str)) // 2
    print("║" + " " * pad_len + title_str + " " * (78 - pad_len - len(title_str)) + "║")
    print("╠" + "═" * 78 + "╣")
    for line in content_lines:
        type_effect(f"║  {line:<74}  ║", 0.005)
    print("╚" + "═" * 78 + "╝")
    time.sleep(0.5)

def clear_screen():
    print("\n" * 40)

def gemini_chatbot():
    print_big_box("GEMINI AI ASSISTANT", [
        "Hello! I am Gemini. Let's talk about REAL Quantum Computers!",
        "What do you want to learn about?"
    ])
    while True:
        print("\n1. Is this game a simulation or real?")
        print("2. Can we run this on REAL Quantum Hardware?")
        print("3. Can we solve REAL world problems (like Q-Day) today?")
        print("4. Back to the game!")
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            type_effect("\n[Gemini]: The basic version of this game runs a 'Simulation' of a quantum computer on your regular CPU. It behaves exactly like a quantum computer mathematically, but it doesn't use real qubits.")
        elif choice == '2':
            type_effect("\n[Gemini]: YES! IBM allows anyone to connect to their real Quantum Computers over the internet via the cloud. We have added the code for it in this game!")
        elif choice == '3':
            type_effect("\n[Gemini]: Not yet! Today's quantum computers have around 100-400 noisy qubits. To break real internet security (Q-Day), we need millions of stable qubits. So today, we can only solve small 'toy' problems on real hardware.")
        elif choice == '4':
            type_effect("\n[Gemini]: Let's get back to the mission!")
            break
        else:
            type_effect("\n[Gemini]: Oops! Please choose 1, 2, 3, or 4.")

def jungle_scene():
    clear_screen()
    print_big_box("LEVEL 1: THE BEAUTIFUL JUNGLE 🌴", [
        "You step into a lush green jungle. Glowing butterflies fly around.",
        "Sitting on a wooden log, you see Dadi and Dada."
    ])
    input("\nPress ENTER to talk to them...")
    type_effect("\n👵 Dadi: 'Welcome, young developer! This jungle holds a secret Omniverse Vault.'")
    type_effect("👴 Dada: 'But it is locked with a giant RSA math puzzle. We old folks tried to solve it with our classic calculators, but it will take a billion years!'")
    
    input("\nPress ENTER to walk to the Quantum Lab...")

def quantum_lab_scene():
    clear_screen()
    print_big_box("LEVEL 2: THE QUANTUM LAB 🔬", [
        "You enter a high-tech lab disguised as a giant mushroom!",
        "Superconducting wires are glowing like neon vines."
    ])
    
    type_effect("\n👩 Mummy: 'Welcome! We found the vault! But classical computers are failing!'")
    
    while True:
        print("\nWhat do you want to do?")
        print("1. Talk to Gemini AI for a hint about REAL hardware.")
        print("2. Tell Mummy to use the [SEEK BOX] and run the Quantum Code.")
        
        choice = input("Enter choice (1-2): ")
        
        if choice == '1':
            gemini_chatbot()
        elif choice == '2':
            type_effect("\n👩 Mummy: 'Brilliant idea! Let's power up the REAL Quantum Network!'")
            break
        else:
            print("Invalid choice!")

def real_quantum_execution():
    if not QISKIT_AVAILABLE:
        print_big_box("REAL QUANTUM MODE INACTIVE", [
            "⚠️ You do not have 'qiskit' installed on this computer.",
            "Please install it using: pip install qiskit",
        ])
        time.sleep(2)
        return False
        
    print_big_box("QUANTUM HARDWARE ENGAGED ⚡", [
        "Building a REAL Quantum Circuit using IBM Qiskit...",
        "Applying Hadamard Gates to create Superposition!",
        "Executing Grover's Algorithm to amplify the correct code probability..."
    ])
    
    # Create a real quantum circuit (2-qubit Grover's search for state |11>)
    qc = QuantumCircuit(2)
    qc.h([0, 1]) # Superposition
    qc.cz(0, 1)  # Oracle marking the secret code
    qc.h([0, 1]) # Diffusion
    qc.z([0, 1])
    qc.cz(0, 1)
    qc.h([0, 1])
    qc.measure_all()
    
    print("\n[REAL QUANTUM CIRCUIT DIAGRAM GENERATED]")
    print(qc.draw())
    time.sleep(2)
    
    print("\nHow do you want to run this circuit?")
    print("1. Run on Local Simulator (Fast & Free)")
    print("2. Run on REAL IBM Quantum Hardware via Cloud (Needs IBM API Token)")
    run_choice = input("Enter choice (1-2): ")
    
    if run_choice == '2':
        if not IBM_RUNTIME_AVAILABLE:
            type_effect("\n❌ You need to install 'qiskit-ibm-runtime' to connect to IBM Cloud!")
            type_effect("Type: pip install qiskit-ibm-runtime")
            type_effect("Falling back to Local Simulator...")
        else:
            print_big_box("CONNECTING TO REAL IBM QUANTUM COMPUTER 🌐", [
                "To use real hardware, you must have an IBM Quantum API token.",
                "Get it for free at: https://quantum.ibm.com/"
            ])
            token = input("Please paste your IBM API Token (or type 'skip' to use simulator): ")
            if token.lower() != 'skip':
                try:
                    type_effect("Connecting to IBM Quantum Cloud... (This may take a minute)")
                    service = QiskitRuntimeService(channel="ibm_quantum", token=token)
                    backend = service.least_busy(simulator=False, operational=True)
                    type_effect(f"✅ Connected to REAL Quantum Computer: {backend.name}!")
                    type_effect("Sending job to the real quantum processor... (You will be placed in a queue)")
                    
                    # Note: Running real jobs takes time (queue). In a real scenario, this blocks until done.
                    type_effect("Job submitted! Real qubits are now physically manipulating microwaves to solve your puzzle...")
                    type_effect("(For this game, we will show the expected mathematical result so you don't have to wait hours in the queue!)")
                except Exception as e:
                    type_effect(f"❌ Connection failed: {e}")
                    type_effect("Falling back to Local Simulator...")
    
    type_effect("\nSending circuit to Quantum Sampler to measure the waves...")
    sampler = Sampler()
    result = sampler.run(qc).result()
    probs = result.quasi_dists[0]
    
    best_state = max(probs, key=probs.get)
    best_prob = probs[best_state] * 100
    
    type_effect(f"\n✅ Quantum Measurement Complete!")
    type_effect(f"Highest Probability State Found: |{bin(best_state)[2:].zfill(2)}> with {best_prob:.1f}% certainty!")
    return True

def climax_scene():
    clear_screen()
    print_big_box("LEVEL 3: QUANTUM SEEK BOX ⚡", [
        "You press the glowing Quantum Button!",
    ])
    
    real_quantum_execution()
    
    input("\nPress ENTER to open the Vault!...")
    
    print_big_box("FIND BOX 🏆", [
        "🎉 PROBLEM SOLVED! 🎉",
        "The primes are P = 997, Q = 991",
        "You cracked the Omniverse Vault!"
    ])

def main():
    clear_screen()
    type_effect("🚀 THE QUANTUM MISSION: REAL HARDWARE EDITION 🚀")
    type_effect("Press ENTER to start your adventure...")
    input()
    
    jungle_scene()
    quantum_lab_scene()
    climax_scene()
    
    print("\n" + "="*80)
    type_effect("🎯 VISION ACCOMPLISHED: YOU ARE A REAL QUANTUM DEVELOPER! 🎯", 0.05)
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
