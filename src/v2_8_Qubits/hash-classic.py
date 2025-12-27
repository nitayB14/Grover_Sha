# -*- coding: utf-8 -*-
"""
Created on Sat Jul 19 00:12:10 2025

@author: ניתאי
"""
from collections import defaultdict


def show_hash_collisions():
    """
    מדפיסה עבור כל פלט של פונקציית ההאש:
    - כמה פעמים הוא חזר
    - אילו קלטים הביאו אליו
    """
    collision_map = defaultdict(list)

    for i in range(256):
        input_bin = format(i, '08b')
        output = bit_hash_8bit(input_bin)
        collision_map[output].append(input_bin)

    sorted_map = sorted(collision_map.items(), key=lambda x: (-len(x[1]), x[0]))

    print(f"\n🔍 זיהוי התנגשויות בפלטים של פונקציית ההאש:\n{'-'*50}")
    for i, (hash_out, inputs) in enumerate(sorted_map, 1):
        print(f"{i:02d}. Output: {hash_out} | Occurrences: {len(inputs)} | Inputs: {', '.join(inputs)}")
    print(f"\n✅ סה״כ פלטים ייחודיים: {len(sorted_map)} מתוך 254 קלטים אפשריים\n")
    
    
def bit_hash_8bit(bitstring: str) -> str:
    """
    פונקציית האש על קלט של 8 ביטים שמחזירה פלט בגודל 8 ביטים.
    כולל הדפסות ביניים של מצב המשתנה state לצורכי דיבאג.
    """
    assert len(bitstring) == 8 and set(bitstring) <= {'0', '1'}, "Input must be 8-bit binary string"

    # חילוץ ערכים
    #state = 0b01010111 # 
    state = 0b11100101  #
    value = int(bitstring, 2)

    #print(f"state:            {bin(state)[2:].zfill(6)}")
    # שלב 1: XOR ראשוני
    
    state ^= value
    
    
    #print(f"After XOR:        {bin(state)[2:].zfill(8)}")
    #print(f"state: {bin(state)}, value: {bin(value)}")

    
    # שלב 2: רוטציה של 2 ביטים שמאלה
    state = ((state << 2) | (state >> 6)) & 0b11111111
    #print(f"After rotate:     {bin(state)[2:].zfill(8)}")
    #print(f"state: {bin(state)}, value: {bin(value)}")

    #print(f"state: {state}, value: {value}")
    # שלב 3: הוספה של value * 7
    state = state + value & 0b11111111
    #print(f"After add:     {bin(state)[2:].zfill(8)}")
    #print(f"state: {bin(state)}, value: {bin(value)}")
    
    
    
    #another shift
    state = ((state << 2) | (state >> 6)) & 0b11111111
    #print(f"After rotation:     {bin(state)[2:].zfill(8)}")
    #print(f"state: {bin(state)}, value: {bin(value)}")
    
    #another xor
    state ^= value
    #print(f"After XOR:        {bin(state)[2:].zfill(6)}")
    #print(f"state: {bin(state)}, value: {bin(value)}")
    
    return bin(state)[2:].zfill(8)



def find_inputs_with_leading_zeros(n: int):
    matches = []
    for i in range(256):
        input_bin = format(i, '08b')
        output = bit_hash_8bit(input_bin)
        print(f"input: {str(bin(i))[2:]} , output: {output}")
        if output.startswith('0' * n):
            matches.append((input_bin, output))
    return matches



def main():
    
    """
    for i in range(64):
        
        binary = format(i, '06b')
        
        result = bit_hash_8bit(binary)
        print(f"input: {binary} , output: {result}")
    """
      
    value = "01101001"
    result = bit_hash_8bit(value)
    print(f"input: {value} , output: {result}")


    
    """
    results = find_inputs_with_leading_zeros(2)
    
    for i, (inp, outp) in enumerate(results):
        print(f"{i+1:02d}. Input: {inp} -> Output: {outp}")
    show_hash_collisions()
    """
    
main()