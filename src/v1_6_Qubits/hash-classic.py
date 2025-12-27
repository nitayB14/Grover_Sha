# -*- coding: utf-8 -*-
"""
Spyder Editor


-----------------------------
Creator: Nitay B.
Date:    27.12.2025
-----------------------------

Explanation: This file is the classic function that we try to convert to grover
             With it we can also check if our grover algorithm worked.
"""

    
def bit_hash_6bit(bitstring: str) -> str:
    """
    Explanation: This function apply the sha function we want

    Parameters
    ----------
    bitstring : str
        string of bits.

    Returns
    -------
    str
        string of bits.

    """
    assert len(bitstring) == 6 and set(bitstring) <= {'0', '1'}, "Input must be 6-bit binary string"

    #state = 0b010101 # 
    state = 0b110011  #
    value = int(bitstring, 2)
    
    #xor
    state ^= value
    #print(f"After XOR:        {bin(state)[2:].zfill(6)}")
    #print(f"state: {bin(state)}, value: {bin(value)}")

    #shift
    state = ((state << 2) | (state >> 4)) & 0b111111
    #print(f"After rotate:     {bin(state)[2:].zfill(6)}")
    #print(f"state: {bin(state)}, value: {bin(value)}")
    
    #add
    state = state + value & 0b111111
    #print(f"After add:     {bin(state)[2:].zfill(6)}")
    #print(f"state: {bin(state)}, value: {bin(value)}")
    
    #shift
    state = ((state << 2) | (state >> 4)) & 0b111111
    #print(f"After rotation:     {bin(state)[2:].zfill(6)}")
    #print(f"state: {bin(state)}, value: {bin(value)}")
    
    #xor
    state ^= value
    #print(f"After XOR:        {bin(state)[2:].zfill(6)}")
    #print(f"state: {bin(state)}, value: {bin(value)}")
    
    return bin(state)[2:].zfill(6)



def find_inputs_with_leading_zeros(n: int):
    """
    Explanation: This function find every input for prefix 0 as output

    Parameters
    ----------
    n : int
        number of prefix - 0.

    Returns
    -------
    matches : TYPE
        returning the input we need for output of prefix 0.

    """
    
    matches = []
    for i in range(64):
        input_bin = format(i, '06b')
        output = bit_hash_6bit(input_bin)
        #print(f"input: {str(bin(i))[2:]} , output: {output}")
        if output.startswith('0' * n):
            matches.append((input_bin, output))
    return matches



def main():
    """
    Explanation:
        This function responsible for creating the sha function for 6 qubits data/nonce
    """

    value = "110101"
    result = bit_hash_6bit(value)
    print(f"nonce: {value} , output: {result}")


    """
    #using in case we want to see all collision
    
    prefix = 4
    results = find_inputs_with_leading_zeros(prefix)
    print(f"outputs with prefix: {prefix}")
    for i, (inp, outp) in enumerate(results):
        print(f"{i+1:02d}. Input: {inp} -> Output: {outp}")
    """
    
main()