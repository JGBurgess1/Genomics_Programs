def get_seq_dictionary(file):
    key = ""
    value = ""
    seq_dict = {}
    start = False
    with open (file) as seq_file:
        for line in seq_file:
            line = line.strip()
            if line.startswith(">"):
                if not len(line) > 1:
                    print(f"{line} is empty, please provide a name for the sequence!")
                else:
                    key = line.split()[0][1:]
                    value = ""
            else:
                value += line
                seq_dict.update({key: value})
    return seq_dict

def get_shortest(start, dict):
    short_key = ""
    num_this_size = 0
    for key, value in dict.items():
        length = len(value)
        if length < start:
            start = length
            short_key = key
            num_this_size = 1
        elif length == start:
            num_this_size += 1
    return short_key, num_this_size, start #, dict.get(short_key)""

def get_longest(start, dict):
    long_key = ""
    num_this_size = 0
    for key, value in dict.items():
        length = len(value)
        if length > start:
            start = length
            long_key = key
            num_this_size = 1
        elif length == start:
            num_this_size+=1
    return long_key, num_this_size, start #, dict.get(long_key)

def get_orfs(seq_dict, frame):
    orf_dict = seq_dict.fromkeys(seq_dict.keys())
    

    frame_shift_dict = seq_dict.copy()
    #print(frame_shift_dict)

    if frame not in [1, 2, 3]:
        print("Error with frame, please enter a frame from 1, 2 or 3")
        exit()
    
    for key in frame_shift_dict.keys():
        frame_shift_dict[key] = frame_shift_dict[key][frame-1:]

    # works to here.

    # orf_dict = {}

    for key in frame_shift_dict.keys():
        seq = frame_shift_dict[key]
        orfs = {}
        start = False
        count = 0
        orf = ""
        for i in range(0, len(seq)-2, 3):
            # codon set up
            # for loop needed fixing.
            codon = seq[i]+seq[i+1]+seq[i+2]
            if codon == 'ATG':
                orf += codon
                start = True
            elif codon in ['TAG', 'TAA', 'TGA']:
                if start:
                    orf += codon
                    count+=1   
                    # return an orf
                    orfs[count] = orf
                    start = False
                    orf = ""
            elif start:
                orf += codon
            else:
                # if not in an orf, keep going to next codon
                pass
        orf_dict[key]=orfs
    return orf_dict
            
    # get the sequence into frame

def get_longest_orf_in_file(seq_dict):
    max_length = 0
    max_length_seq_id = ""
    max_length_orf_key = ""
    for key in seq_dict:
        if seq_dict[key] == {}:
            pass
        else:
            for orf_key in seq_dict[key]:
                length = len(seq_dict[key][orf_key])
                if length > max_length:
                    max_length_seq_id = key
                    max_length = length
                    max_length_orf_key = orf_key
    return max_length_seq_id, max_length_orf_key, max_length

def get_longest_orf_for_seq_key(seq_dict, orf_dict, seq_id):
    # get both the length of the longest orf
    # and the position in the seq for which it starts
    # use a find() method with the orf as the template.
    # + 1, as it starts with 0. - They weren't clear with that in the instructions.
    max_length = 0
    max_length_orf_key = ""
    if orf_dict[seq_id] == {}:
        return f"No ORFs detected in this sequence: {seq_id}"
    else:
        for orf_key in orf_dict[seq_id]:
            length = len(orf_dict[seq_id][orf_key])
            if length > max_length:
                max_length = length
                max_length_orf_key = orf_key

    position = seq_dict[seq_id].find(orf_dict[seq_id][max_length_orf_key])+1
    # +`1 for the position?`
    return max_length_orf_key, max_length, position

def find_all_subsequences(seq_dict, N):
    subsequences = {}
    for key in seq_dict:
        for i in range(len(seq_dict[key])-N):
            subsequence = seq_dict[key][i:i+N]
            subsequences[subsequence] = 0
    return subsequences

def get_num_repeats(N, seq_dict):
    #sequences = generate_dna_sequences_recursive(N)
    sequences = find_all_subsequences(seq_dict, N)
    max_num_repeats = 0
    max_num_repeats_seq = ""

    num_seqs = 0

    for substring in sequences.keys():
        positions = []
        for key in seq_dict:
            start = 0
            while True:
                start = seq_dict[key].find(substring, start)
                if start == -1: # i.e. is not found,
                    break
                start += 1
                positions.append(start)
        if len(positions) > max_num_repeats:
            max_num_repeats = len(positions)
            max_num_repeats_seq = substring
        sequences[substring]=len(positions)
    
    for key in sequences:
        if sequences[key]==max_num_repeats:
            num_seqs += 1
    #print(sequences)
    return max_num_repeats, max_num_repeats_seq, num_seqs


def generate_dna_sequences_recursive(length): # long, and takes far too long for sequences more than 10 bases in length!
  # See the find_all_subsequences method above.
  """Recursive function, genereated by Gemini, to generate all possible DNA sequences of a given length. 
  Args:
    length: The desired length of the DNA sequences.
  Returns:
    A dictionary with keys of all possible DNA sequences, and 0 occurences for each key.
  """
  nucleotides = ['A', 'C', 'G', 'T']
  sequences = {}

  def generate_sequence(current_sequence):
        if len(current_sequence) == length:
            sequences[current_sequence] = 0
            return

        for nucleotide in nucleotides:
            generate_sequence(current_sequence + nucleotide)

  generate_sequence("")
  #print(sequences)
  return sequences

if __name__ == "__main__":
    seq_dict = get_seq_dictionary("dna2.fasta")
    #print(seq_dict.get(">gi|142022655|gb|EQ086233.1|521 marine metagenome JCVI_SCAF_1096627390048 genomic scaffold, whole genome shotgun sequence"))
    print(len(seq_dict))

    print(f"The shortest seq in the file: {get_shortest(2000, seq_dict)}")
    print(f"The longest seq in the file: {get_longest(0, seq_dict)}")

    orf_dict = get_orfs(seq_dict, 1)

    print(f"The longest ORF in the file: {get_longest_orf_in_file(orf_dict)}")
    seq_id = 'gi|142022655|gb|EQ086233.1|527'
    print(f"The longest ORF for seq_id {seq_id} is: {get_longest_orf_for_seq_key(seq_dict, orf_dict, seq_id)}")

    seq_id = 'gi|142022655|gb|EQ086233.1|16'
    print(f"The longest ORF for seq_id {seq_id} is: {get_longest_orf_for_seq_key(seq_dict, orf_dict, seq_id)}")
    
    N_seqs = 12
    print(f"The most repeated sequence of N={N_seqs} is {get_num_repeats(N_seqs, seq_dict)}")