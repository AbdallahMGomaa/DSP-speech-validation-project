# speech validation project
## for digital signal processing applications course EECE cairo university
#### a user should record 61 pairs of words (122 words) with similar pronunciation and a single reference word so total of 123 words.
the system should load the precalculated MFCC files for reference speakers and test speakers and calculate how many words did the test speaker pronounced correct,
and then plot the mismatches in frames of the wrongly mismatched words.
the system uses DTW (dynamic time warping) algorithms with constraints on direction of motion in vertical or horizontal directions with just one step.
DTW returns the minimum cost to reconstruct the input signal to match the size of the reference signal
