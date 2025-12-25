from qiskit import *
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from math import pi
from qiskit.quantum_info import Statevector, partial_trace
from qiskit.circuit.library import ZGate




def print_measurements(qc):
    #qc.measure([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    #qc.measure([0,1,2,3,4,5,15],[0,1,2,3,4,5,6])
    #qc.measure([7,8,9,10,11,12,15], [0,1,2,3,4,5,6])
    #qc.measure(state, state)
    #qc.measure(value, state)
    
    
    qc.draw(output="mpl")

    
    
    simulation = Aer.get_backend('qasm_simulator')
    transpiled_qc = transpile(qc, simulation)
    
    #run the simulation
    job = simulation.run(transpiled_qc, shots=4096)
    #get result
    result = job.result()
    counts = result.get_counts()
    
    #print the results
    #plot_histogram(counts)
    flipped_counts = {key[::-1]: value for key, value in counts.items()}
    plot_histogram(flipped_counts)

    print(flipped_counts)

checking_ancilla_2 = 6
checking_ancilla = 5
ancilla = 4
q = [0,1,2,3]
    
def oracle(qc):
    
    qc.x(q[0])
    qc.x(q[1])
    
    qc.mcx([q[0],q[1], q[2]], ancilla)
    qc.z(ancilla)
    qc.mcx([q[0], q[1], q[2]], ancilla)
    
    qc.x(q[1])
    qc.x(q[0])
    
    
    
def diffuser(qc):
    
    qc.h(q)
    qc.x(q)
    
    """
    qc.ccx(q[0], q[1], checking_ancilla)
    qc.ccx(q[2], q[3], checking_ancilla_2)
    
    qc.h(q[4])
    qc.ccz(checking_ancilla, checking_ancilla_2, q[4])
    qc.h(q[4])

    qc.ccx(q[2], q[3], checking_ancilla_2)
    qc.ccx(q[0], q[1], checking_ancilla)
    """
    
    """
    4 qubits diffuser
    """
    
    control_qubits = [q[0], q[1], q[2]]
    target_qubit = q[3] # One target qubit
    

    
    #qc.ccx(q[0], q[1], checking_ancilla)
    qc.h(q[3])
    #qc.ccz(checking_ancilla, q[2], q[3])
    qc.append(ZGate().control(3), control_qubits + [target_qubit])

    qc.h(q[3])
    #qc.ccx(q[0], q[1], checking_ancilla)
    
    
    
    
    """
    3 qubits diffuser
    
    qc.ccx(q[0], q[1], ancilla)    
    qc.h(q[2])
    qc.cz(ancilla, q[2])
    qc.h(q[2])
    qc.ccx(q[0], q[1], ancilla)
    """
    qc.x(q)
    qc.h(q)
    
    

def main():
    
    qc = QuantumCircuit(6, 4)
    
    qc.h(q)
    
    for i in range(1):
        oracle(qc)
        qc.barrier()
        
        diffuser(qc)
        qc.barrier()
    
    
    qc.measure([0, 1, 2, 3], [0, 1, 2, 3])
    
    print_measurements(qc)
    
    
main()