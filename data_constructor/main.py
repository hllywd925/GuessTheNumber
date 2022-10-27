def read_data(file):
    with open(file) as f:
        f = f.read()
        return f


print(read_data('user.txt'))
