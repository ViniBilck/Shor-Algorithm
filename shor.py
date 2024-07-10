from math import gcd, pi
from random import randint
from functools import reduce
from ket import H, PHASE, SWAP, Process, X, adj, measure, ctrl

class Shor:
    def __init__(self, number_to_be_factored):
        self.number_to_be_factored = number_to_be_factored
        self.factored = self.shor(self.number_to_be_factored)


    def inverse_qft(self, qubits):
        n = len(qubits)
        for i in range(n // 2):
            SWAP(qubits[i], qubits[n - i - 1])
        for i in range(n):
            H(qubits[i])
            for j in range(i + 1, n):
                angle = -pi / (2 ** (j - i))
                ctrl(qubits[j], PHASE(angle))(qubits[i])

    def quantum_subroutine(self, qbits_number):
        process = Process()
        qubits = process.alloc(qbits_number)
        reg1 = H(qubits)
        reg2 = X(reg1[-1])
        measure(reg2)
        adj(self.inverse_qft)(reg1)
        return measure(reg1).value


    def shor(self, factor_number):
        number_of_qbits = factor_number.bit_length()

        for _ in range(number_of_qbits):
            x = randint(2, factor_number - 1)
            rr = reduce(gcd, [self.quantum_subroutine(number_of_qbits) for _ in range(number_of_qbits)])
            try:
                r = 2 ** number_of_qbits // rr
                # novo processamento clássico
                if r % 2 == 0:
                    x_r_over_2 = pow(x, r // 2, factor_number)
                    if x_r_over_2 != factor_number - 1:
                        p = gcd(x_r_over_2 - 1, factor_number)
                        if p != 1 and p != factor_number:
                            return p, 'quantum'

                        q = gcd(x_r_over_2 + 1, factor_number)
                        if q != 1 and q != factor_number:
                            return q, 'quantum'
            except:
                continue

        return factor_number, 'prime or fail'

if __name__ == "__main__":
    N = 13680
    shor = Shor(N)
    factor, message = shor.factored
    print(f'N: {N:2} = {factor:2} * {N // factor:2} ({message})')