import random, json

ratio = 0.2 # percentage of testset, the rest will be trainset

file = "log/full.json"
with open(file, "r") as f:
    records = json.load(f)

random.shuffle(records)

testset = records[:int(ratio*len(records))]
trainset = records[int(ratio*len(records)):]

with open("testset.json", "w+") as f:
    json.dump(testset, f)
with open("trainset.json", "w+") as f:
    json.dump(trainset, f)