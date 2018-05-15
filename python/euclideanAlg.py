import sys

#gcd(a,b) = gcd(b, a%b) sii a>b
#caso base : si a%b = 0 => gcd(b,0) = b
def gcd(a,b):
    if b == 0:
        return a
    else:
        return gcd(b, a%b)

#egcd(a,b)=s*a+t*b
#devuelve 3 valores g,s,t
#caso base: a%b = 0 ; gcd(a,0) => g = s*a + t*b = a => s=1, t=0
#gcd(ri+1,ri) = gcd(ri+2,ri+1) sii Ri+2 = Qi+1*Ri+1 + Ri
#gcd(r1,r0) = S0*R1 + T0*R0
# Si*Ri+1 + Ti*Ri = Si+1*Ri+2 + Ti+1*Ri+1
# Si*Ri+1 + Ti*Ri = Si+1*(Qi+1*Ri+1 + Ri) + Ti+1*Ri+1
# Si*Ri+1 + Ti*Ri = Si+1*Qi+1*Ri+1 + Si+1*Ri + Ti+1*Ri+1
# Si*Ri+1 + Ti*Ri = Ri+1[Si+1*Qi+1 + Ti+1] + Ri[Si+1]
# Si = Si+1*Qi+1 + Ti+1 ; Ti = Si+1
# Si+1 = Ti
# Ti+1 = Si - Si+1*Qi+1
def egcd(a,b):
    if b==0:
        return (a,1,0)
    else:
        g,s,t = egcd(b, a%b)
        q = a//b
        s1 = t
        t1 = s - (q*t)
        print('-------------********-')
        print(s)
        print(t)
        print(q)
        print(a)
        print(b)
        print(s1)
        print(t1)
        print('--------------')
        return (g,s1,t1)


if __name__ == "__main__":
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    if (a>b):
        g = gcd(a,b)
        print (g)
        g,s,t = egcd(b,a)
        print(s)
        print(t)
    else:
        print("fallo")
