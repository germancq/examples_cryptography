import sys

#input: matrix M nxm = [A|b]
# Mij i= row j=colunm
#[4   6   2]
#[3   9   1]
#M12 = 6  === M[0][1]
#M = [[row][row][row]]
#Alg
M_result=[]

def gauss_jordan_elimination(M):
    reduced_row_echelon_form(M)


def has_unique_solution(M):
    for elem in M[len(M)-1]:
        if elem != 0:
            return True
    return False

def has_solution(M):
    for i in reversed(range(0,len(M))):
        if M[i][len(M[0])-1] == 0:
            continue
        for j in reversed(range(0,len(M[0])-1)):
            if M[i][j] != 0:
                return True
        return False

def row_echelon_form(M):
    pivoting_down(M,0)


def reduced_row_echelon_form(M):
    row_echelon_form(M)
    M_up = M_result[:]
    pivoting_up(M_up,0)

def pivoting_down(M,k):
    leftmost_value = sort_row_matrix(M)
    if leftmost_value == 0:
        for row_index in range(0,len(M)):
            for colunm_index in range(0,k):
                M_result[row_index+k][colunm_index] = 0.0
            M_result[row_index+k][k:] = M[row_index]
        return
    else:
        if leftmost_value != 1:
            M[0] = scaling_row(M[0],1/leftmost_value)
        #make the leftmost colunm for i>0 be 0
        for i in range(1,len(M)):
            colunm_value = M[i][0]
            if colunm_value != 0:
                replace_row(M,i,0,colunm_value)

        for colunm_index in range(0,k):
            M_result[k][colunm_index] = 0.0
        M_result[k][k:] = M[0]
        k +=1

        newM = M[1:]
        for x in range(0,len(newM)):
            newM[x] = newM[x][1:]

        pivoting_down(newM,k)


def pivoting_up(M,k):
    row,colunm = search_pivot(M)
    print(M)
    print(row,colunm)
    if row == 0:
        return
    else:
        #make the colunm of the pivot equal 0 for the rows above
        for i in range(0,row):
            colunm_value = M[i][colunm]
            print(colunm_value)
            if colunm_value != 0:
                replace_row(M,i,row,colunm_value)

        M_result[row] = M[row]
        new_M = M[0:row]
        k += 1

        pivoting_up(new_M,k)

def search_pivot(M):
    for i in reversed(range(0,len(M))):
        for j in reversed(range(0,len(M[0]))):
            candidate = M[i][j]
            if candidate == 1:
                return i,j
    return 0,0

def sort_row_matrix(M):
    leftmost_value = 0
    #left colunm must be non-zero
    for i in range(0,len(M)):
        leftmost_value = M[i][0]
        if leftmost_value != 0:
            swap_rows(M,0,i)
            break
    #swap row 0 to row i
    return leftmost_value


#operations:
#swap Ri <-> Rj
#scaling Ri*S -> Ri
#replace Ri − S*Rj -> Ri
def swap_rows(M,ri,rj):
    row_i = M[ri]
    row_j = M[rj]
    M[ri] = row_j
    M[rj] = row_i

def scaling_row(r,s):

    return [s * elem for elem in r]

def replace_row(M,ri,rj,s):
    r = scaling_row(M[rj],s)
    for k in range(0,len(M[0])):
        M[ri][k] = M[ri][k] - r[k]



if __name__ == "__main__":
    #M = [[1.0,1.0,1.0,6.0],[1.0,-2.0,3.0,6.0],[4.0,-5.0,6.0,12.0]]
    M = [[1.0,2.0,3.0],[4.0,5.0,6.0],[7.0,8.0,9.0]]
    M_result = M[:]
    gauss_jordan_elimination(M)

    print(M_result)
