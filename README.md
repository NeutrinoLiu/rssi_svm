quick start:
- install all requirements
- run autotest.sh, which will test with offline dataset raw/full.json

trainer.py for training SVM model, which will be stored in svm.pickle
judger.py for test SVM model, using svm.pickle at the directory
spitter is used to generate testset and trainset from full.json