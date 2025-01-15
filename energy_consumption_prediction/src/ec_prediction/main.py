DATA_DIR = "data/"
fname = DATA_DIR + "PJMW_hourly.csv"
f = open(fname)
data = f.read()
f.close()
lines = data.split("\n")
header = lines[0].split(",")
lines = lines[1:]
print(header)
print(len(lines))
