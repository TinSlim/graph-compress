import gzip
from itertools import islice

###Abrir gzip
SUBSETS = [1000000000, 100000000, 10000000, 1000000, 100000, 10000]
TOTAL_LINES = 7341099184

line_counter = 0
line_added = 0

cache_files = []
for sub in SUBSETS:
	cache_files.append(gzip.open(f"subset{sub}.nt.gz","wb"))

cache_small = gzip.open("small_lt.nt.gz","wb")

with gzip.open('../latest-truthy.nt.gz','r') as f:
	for line in f:
		line_decode = line.decode()
		line_split = line_decode.split(" ")
		if '<http://www.wikidata.org/entity/Q' == line_split[0][:33] and \
			'<http://www.wikidata.org/prop/direct/P' == line_split[1][:38] and \
			'<http://www.wikidata.org/entity/Q' == line_split[2][:33]:
				subj = int(line_split[0][33:-1])
				pred = int(line_split[1][38:-1])
				obj  = int(line_split[2][33:-1])

				for index in range(len(SUBSETS)):
					if (subj <= SUBSETS[index] and obj <= SUBSETS[index]):
						cache_files[index].write(line)

				cache_small.write(line)
				line_added += 1

		line_counter += 1
		print(f"{line_counter}/{TOTAL_LINES}  {(line_counter * 100) // TOTAL_LINES}%", end="\r")
print(f"Total {line_counter} lineas")
print(f"Total {line_added} lineas agregadas")
