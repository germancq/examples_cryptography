import sys
import euclideanAlg

def euler_totient_function(n):
    result = 0
    for i in range(1,n+1):
        if euclideanAlg.gcd(n,i) == 1:
            result +=1
    return result

def maximum_primitives_polynomials(base,degree):
    totient = euler_totient_function(base**degree - 1)
    return totient/degree




if __name__ == "__main__":
    value = maximum_primitives_polynomials(2,int(sys.argv[1]))
    print(value)
