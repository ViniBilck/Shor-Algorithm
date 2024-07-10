from math import gcd, pi
from random import randint
from functools import reduce
from ket import H, PHASE, SWAP, Process, X, adj, measure, ctrl
import argparse
import configparser
import os


class Shor:
    def __init__(self, number_to_be_factored):
        self.number_to_be_factored = number_to_be_factored
        self.factored = self.shor(self.number_to_be_factored)


    def inverse_qft(self, qubits):
        n = len(qubits)
        if len(qubits) != 1:
            for i in range(n // 2):
                SWAP(qubits[i], qubits[n - i - 1])
            for i in range(n):
                H(qubits[i])
                for j in range(i + 1, n):
                    angle = -pi / (2 ** (j - i))
                    ctrl(qubits[j], PHASE(angle))(qubits[i])
        else:
            H(qubits)

    def quantum_subroutine(self, qbits_number):
        process = Process()
        qubits = process.alloc(qbits_number)
        reg1 = H(qubits)
        reg2 = X(reg1[-1])
        measure(reg2)
        self.inverse_qft(reg1)
        return measure(reg1).value


    def shor(self, factor_number):
        number_of_qbits = factor_number.bit_length()

        for _ in range(number_of_qbits):
            x = randint(2, factor_number - 1)
            rr = reduce(gcd, [self.quantum_subroutine(number_of_qbits) for _ in range(number_of_qbits)])
            try:
                r = 2 ** number_of_qbits // rr
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="", dest='config_file', default='config.ini', type=str)
    args = parser.parse_args()
    _dir = os.path.realpath('.')
    config = configparser.ConfigParser(defaults={'here': _dir})
    config.read(args.config_file)
    data = (config.get("Settings", "number"))
    if "..." in data:
        data = [int(numbers) for numbers in (config.get("Settings", "number")).split('...')]
        for result in range(data[0], data[1] + 1):
            N = result
            shor = Shor(N)
            factor, message = shor.factored
            print(f'N: {N:2} = {factor:2} * {N // factor:2} ({message})')
    else:
        numbers = [int(numbers) for numbers in (config.get("Settings", "number")).split(',')]
        for result in numbers:
            N = result
            shor = Shor(N)
            factor, message = shor.factored
            print(f'N: {N:2} = {factor:2} * {N // factor:2} ({message})')