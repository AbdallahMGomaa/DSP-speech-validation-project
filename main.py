"""
    main function:
    - read the input MFCC files
    - split the input MFCC files into u users, p pairs, and 2 words each of
    - detect the reference for each user by using the 122th MFCC vector
    - for each word in pair in user detect whether it is pronounced correctly or not.
    - calculate the accuracy of the system
    - plot where are the differences in frames of an utterence (for n mismatched utterences)
"""

# reading the input MFCC files
