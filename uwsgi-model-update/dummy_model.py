import sys
import os
import dill
import hashlib

class DummyModel(object):
    """
    Dummy model - used to illustrate API model update functionality
    """
    def __init__(self, constant):
        self.constant = constant
        self.hash = hashlib.md5(dill.dumps(self)).hexdigest()
    
    def predict(self, features):
        # ignore features - just return hash value normalized by our constant
        return (hash(str(features)) % 10) / self.constant


if __name__ == "__main__":
    # run as main to generate sample model
    filename = sys.argv[1]
    constant = int(sys.argv[2])
    
    dm = DummyModel(constant)

    with open(filename, 'wb') as f:
        dill.dump(dm, f)
