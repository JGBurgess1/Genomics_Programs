def read_Genome(file):
    genome = ''
    with open(file, 'r') as genome_file:
        for line in genome_file:
            if not line[0] == '>':
                genome += line.rstrip()
    return genome

if __name__ == "__main__":
    genome = read_Genome('lambda_virus.fa')
    print(len(genome))