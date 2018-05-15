import sys
import euclideanAlg



class CustomPRNG:
    def __init__(self, seed):
        self.seed = seed
        self.currentState = seed

    def generateNumber(self):
        self.currentState = self.currentState * 1103515245 + 12345
        return self.currentState % 2**31

class CustomCipher:
    def __init__(self, key):
        self.prng = CustomPRNG(key)

    def encrypt(self,input_text, output_text):
        with open(input_text, 'rb') as myfile:
            data=myfile.read()

        output_file = open(output_text, 'wb')

        for i in range(0,len(data),4):
            x = data[i:i+4]
            encrypt_data = int.from_bytes(x,'big') ^ self.prng.generateNumber()
            output_file.write(encrypt_data.to_bytes(4,'big'))

    def decrypt(self,input_text,output_text,first_decoded_word):
        with open(input_text, 'rb') as myfile:
            data=myfile.read()

        output_file = open(output_text, 'wb')
        original_key = self.calculate_seed(bytes(first_decoded_word, 'utf-8'), data[0:4])
        print(original_key)
        self.prng = CustomPRNG(original_key)

        for i in range(0,len(data),4):
            y = data[i:i+4]
            decrypt_data = int.from_bytes(y,'big') ^ self.prng.generateNumber()
            output_file.write(decrypt_data.to_bytes(4,'big'))

    def calculate_seed(self, x1, y1):
        #S1 = S0 * A + B mod 2**31
        #Y1 = X1 xor S1
        a = 1103515245
        g,s,t=euclideanAlg.egcd(2**31,a)
        print(g)
        print(s)
        print(t)
        inv_a = t%2**31
        print(inv_a)
        b = 12345
        s1 =  int.from_bytes(y1,'big') ^ int.from_bytes(x1,'big')
        print(s1)
        return ((s1-b) * inv_a) % 2**31


if __name__ == "__main__":
    key = int(sys.argv[1])
    print(key)
    input_text = sys.argv[2]
    output_text = sys.argv[3]
    first_decoded = sys.argv[4]
    cipher = CustomCipher(key)
    if key == 0:
        cipher.decrypt(input_text, output_text,first_decoded)
    else:
        cipher.encrypt(input_text, output_text)
