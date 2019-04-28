import cPickle

def write_out(file_path, data):
    with open(file_path, 'wb') as f:
        cPickle.dump(data, f)


