seq_a = "ACCCATTTA"
seq_b = "ACCTTAAGC"

match = 1
mismatch = -1
gap = -2


def make_entry():
    return {"val": 0, "up": None, "left": None, "diag": None}


def make_matrix(seq_a, seq_b):
    mat = []
    for i in range(len(seq_a)):
        m = []
        for j in range(len(seq_b)):
            m.append(make_entry())
        mat.append(m)

    return mat


m = make_matrix(seq_a, seq_b)

def pretty_print(mat):
    for i in range(len(mat)):
        line = mat[i]
        res = "".join(map(lambda x: str(x["val"]), line))
        print(res)

# pretty_print(m)


def main(mat):
    i = 0
    for i in range(len(mat)):
        if i > 1:
            return
        # print(seq_b[i])
        line = mat[i]
        for j in range(len(line)):
            # print(seq_a[j])
            mat[i][j]["up"] = gap * (j + 1)
            mat[i][j]["left"] = gap * (j + 1)
            if i-1 >= 0: 
                # first row
                mat[i][j]["diag"] = gap * (j + 1)
                # print("all good")
            else:
                mat[i][j]["diag"] = 100000000
                print(i,j)
                raise Exception("meh")
                # print("ok",i,j)
            # find best one
            keys_to_sort = ["up", "left", "diag"]
            ordered = sorted([mat[i][j][k] for k in keys_to_sort])
            mat[i][j]["val"] = ordered[-1]
            print(ordered)
            # print("val",mat[i][j]["val"])
        i = i + 1


print("\n=========\n")
main(m)
pretty_print(m)
