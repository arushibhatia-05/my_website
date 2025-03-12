# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: Python [conda env:base] *
#     language: python
#     name: conda-base-py
# ---

# Problem 1:
# a) If we want to have an output of 20 bits, how many hex characters should we have in the output of
# the new hash function?
# b) Import the hashlib package in Python.Compute the sha256 of "hello world". 
# c) Create a function that returns the first “k” characters of the digest of the SHA256 function. Call the
# function mod_hash. The function should have two arguments: the text to be hashed and the number
# of characters of the output (k).
#

# +
#part a: 
#one hex = 4bits = 0.5 bytes

twenty_bits = 20/4
print("The ouput should have", twenty_bits, "hex characters")


# +
#partb:
import hashlib

mytext="hello world"
thedigest=hashlib.sha256(mytext.encode()).hexdigest() 
print(thedigest)


# -

#part c
def mod_hash(text, k):
    return hashlib.sha256(text.encode()).hexdigest()[:k]


mod_hash("hello world",9)


# Problem 2: Guessing the number (i.e., attacking the function)
# a) Guess the number of this month’s raffle.
# b) Find a number so that the digest of this month’s draw has four leading zeros (i.e., that the first 4
# digits are 0 and the fifth is any number)
# c) Suppose now that the Mass Lottery uses the mod_hash() using the first 7 hex characters of the
# sha256. Find the first integer that leads to the following digest “00a4c03”

#part a
def find_matching_number(target_digest, k):
    for num in range(1,1000000):
        hashed_value = mod_hash(generate_message(num), k)
        if hashed_value == target_digest:
            return num  
    return None 



find_matching_number('00a4c', 5)


#verify part a
def verify_number(number, target_digest, k):
    message = generate_message(number)
    hashed_value = mod_hash(message, k)
    return hashed_value == target_digest


verify_number(1020570,'00a4c', 5)


#partb
def find_prefix(target_prefix, k):
    for num in range(1,1000000):  
        hashed_value = mod_hash(generate_message(num), k)
        if hashed_value.startswith(target_prefix):
            return num  
    return None  


find_prefix('0000', 5)


#part c
def find_matching(target_hash, k):
    for num in range(1,10000000):
        if mod_hash(f"The magic number of the month is {num}", k) == target_hash:
            return num 
    return "No match found"


print(find_matching("00a4c03",len(target_hash_c)))

# Problem 3: Computing the hash rate of your system. Create a loop that goes from 0 to 1,000,000. In each loop, create the following string:
# “this is the iteration [i]” Where “i” is the iteration in the loop. In each iteration, compute the hash of the string (don’t store it). Compute the start and the end time of the program to see compute your hash rate. For this, you need to
# import the package time. To store the time at the beginning of the program, type start=time.time(). To store
# the end time, type end=time.time(). The runtime is simply runtime=end-start. Your hash rate is
# 1,000,000/runtime. This will give you the number of hashes per seconds.

# +
import time

start = time.time()
for i in range(0,1000000):
    text = f"this is the iteration [i]"
    hashlib.sha256(text.encode()).hexdigest()

end = time.time()

runtime = end - start
hash_rate = 1000000 / runtime 

print("Total Runtime:", runtime, "seconds")
print("Hash Rate:", hash_rate, "hashes per second")
# -

# Problem 4: Tug of War
# Country A and Country B are on the verge of war. Country A sent 100,000 troops to the border. B is doing
# the same. The UN wants to broker a de-escalation, however, the parties don’t trust each other. Suppose that
# A sends the following message to B: “I agree to withdraw our forces from the border”. Because A does not
# trust B, A also sends the hashed version of the message using the mod_hash() function.
# B knows that the mod_hash() is not “good” hash function. As such, B wants to forge a message and make
# it look like it was sent by A so that B can start a war with justification.
# To this end, CS in B need to find a message that results in the same hash of the original message sent by A.
#
# a) B is thinking about using the following text as a forged message:
# “Prepare for war! I will send [i] troops to the border”
# Where [i] is the number of troops that supposedly A will send to the border. Find the [i], if any, that leads
# to the same hashed output as the original message.
# Note: If you can find the [i] that leads to the same message digest, then B will show the forged message to
# the UN along with the hash, and war will start (justified)!

# +
original_message = "I agree to withdraw our forces from the border"

# Compute hash of the original message
k_value = 5 
original_hash = mod_hash(original_message, k_value)

# Define the forged message template
def forged_message(i):
    return f"Prepare for war! I will send {i} troops to the border"

# Find 'i' that has the same hash as the original message
def find_forged_message(original_hash, k):
    for i in range(1,10000000):
        forged_hash = mod_hash(forged_message(i), k)
        if forged_hash == original_hash:
            return i  


# +
troops = find_forged_message(original_hash, k_value)

# Print result
if troops != None:
    print(f"Found a forged message! B can claim A sent {troops} troops to the border.")
else:
    print("No forged message found within the search range.")
# -

# Problem 5: Optional ( )
# Find the distribution of the outputs of the mod_hash() functions and export it to Excel. Run a loop that goes
# from 0 to 10,000,000 of the mod_hash() and count the number of times each output shows up. Export the
# output to Excel.
# Is there any output more likely than other?
#

# +
import pandas as pd
hash_distribution = {}
# Compute hash distribution
for i in range(0,10000000):
    hash_output = mod_hash(f"Iteration {i}", k_value)
    if hash_output in hash_distribution:
        hash_distribution[hash_output] += 1
    else:
        hash_distribution[hash_output] = 1

# Convert distribution to DataFrame
df = pd.DataFrame(list(hash_distribution.items()), columns=["Hash Output", "Frequency"])

# Export to Excel (File creation step, but no download)
output_file = "hash_distribution.xlsx"
df.to_excel(output_file, index=False)

# Display the first few rows of the distribution data to check 
print(df.head())
# -

# Because we are using the first 5 digits to see the output I think it does increase the chances of having one specific output over another because the number of unique hash outputs is significantly reduced. Usually a SHA 256 output has 64 characters but since you only output the first 5, the frequency of that will naturally increase. 


