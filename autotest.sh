python3 spliter.py
python3 trainer.py trainset.json | grep CRITICAL
python3 judger.py testset.json | grep CRITICAL
rm log/record*