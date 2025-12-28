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


    
def bit_hash_8bit(bitstring: str) -> str:
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
    
    assert len(bitstring) == 8 and set(bitstring) <= {'0', '1'}, "Input must be 8-bit binary string"

    #data = 0b01010111 # 
    data = 0b00111010  #
    nonce = int(bitstring, 2)

    #xor
    data ^= nonce
    #print(f"After XOR:        {bin(data)[2:].zfill(8)}")
    #print(f"data: {bin(data)}, nonce: {bin(nonce)}")

    #shift
    data = ((data << 2) | (data >> 6)) & 0b11111111
    #print(f"After rotate:     {bin(data)[2:].zfill(8)}")
    #print(f"data: {bin(data)}, nonce: {bin(nonce)}")

    #add
    data = data + nonce & 0b11111111
    #print(f"After add:     {bin(data)[2:].zfill(8)}")
    #print(f"data: {bin(data)}, nonce: {bin(nonce)}")
    
    #shift
    data = ((data << 2) | (data >> 6)) & 0b11111111
    #print(f"After rotation:     {bin(data)[2:].zfill(8)}")
    #print(f"data: {bin(data)}, nonce: {bin(nonce)}")
    
    #xor
    data ^= nonce
    #print(f"After XOR:        {bin(data)[2:].zfill(8)}")
    #print(f"data: {bin(data)}, nonce: {bin(nonce)}")
    
    return bin(data)[2:].zfill(8)



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
    for i in range(256):
        input_bin = format(i, '08b')
        output = bit_hash_8bit(input_bin)
        #print(f"input: {str(bin(i))[2:]} , output: {output}")
        if output.startswith('0' * n):
            matches.append((input_bin, output))
    return matches



def main():
    """
    Explanation:
        This function responsible for creating the sha function for 8 qubits data/nonce
    """
      
    nonce = "10011001"
    result = bit_hash_8bit(nonce)
    print(f"input: {nonce} , output: {result}")
    
    """
    #using in case we want to see all collision
    
    prefix = 5
    results = find_inputs_with_leading_zeros(prefix)
    print(f"outputs with prefix: {prefix}")
    for i, (inp, outp) in enumerate(results):
        print(f"{i+1:02d}. Input: {inp} -> Output: {outp}")
    """
    
main()