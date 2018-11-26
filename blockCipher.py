
class BlockCipher :
    CommonKey = 0
    KeyBitPermutation = [17,35,8,6,41,48,28,20,
                         27,53,61,49,18,32,58,63,
                         23,19,36,38,1,52,26,0,
                         33,3,12,13,56,39,25,40,
                         50,34,51,11,21,47,29,57,44,30,7,24,22,46,60,16,
                         59,4,55,42,10,5,9,43,31,62,45,14,2,37,15,54]
    XOR = [[0,0,0,0,0,0,0,1],
           [0,0,0,0,0,0,1,0],
           [0,0,0,0,0,0,1,1],
           [0,0,0,0,0,1,0,0],
           [0,0,0,0,0,1,0,1],
           [0,0,0,0,0,1,1,0]]
    BlockSBOX = [  0x3a, 0xea, 0x68, 0xfe, 0x33, 0xe9, 0x88, 0x1a, 0x83, 0xcf, 0xe1, 0x7f, 0xba, 0xe2, 0x38, 0x12,

                0xe8, 0x27, 0x61, 0x95, 0x0c, 0x36, 0xe5, 0x70, 0xa2, 0x06, 0x82, 0x7c, 0x17, 0xa3, 0x26, 0x49,

                0xbe, 0x7a, 0x6d, 0x47, 0xc1, 0x51, 0x8f, 0xf3, 0xcc, 0x5b, 0x67, 0xbd, 0xcd, 0x18, 0x08, 0xc9,

                0xff, 0x69, 0xef, 0x03, 0x4e, 0x48, 0x4a, 0x84, 0x3f, 0xb4, 0x10, 0x04, 0xdc, 0xf5, 0x5c, 0xc6,

                0x16, 0xab, 0xac, 0x4c, 0xf1, 0x6a, 0x2f, 0x3c, 0x3b, 0xd4, 0xd5, 0x94, 0xd0, 0xc4, 0x63, 0x62,

                0x71, 0xa1, 0xf9, 0x4f, 0x2e, 0xaa, 0xc5, 0x56, 0xe3, 0x39, 0x93, 0xce, 0x65, 0x64, 0xe4, 0x58,

                0x6c, 0x19, 0x42, 0x79, 0xdd, 0xee, 0x96, 0xf6, 0x8a, 0xec, 0x1e, 0x85, 0x53, 0x45, 0xde, 0xbb,

                0x7e, 0x0a, 0x9a, 0x13, 0x2a, 0x9d, 0xc2, 0x5e, 0x5a, 0x1f, 0x32, 0x35, 0x9c, 0xa8, 0x73, 0x30,

                0x29, 0x3d, 0xe7, 0x92, 0x87, 0x1b, 0x2b, 0x4b, 0xa5, 0x57, 0x97, 0x40, 0x15, 0xe6, 0xbc, 0x0e,

                0xeb, 0xc3, 0x34, 0x2d, 0xb8, 0x44, 0x25, 0xa4, 0x1c, 0xc7, 0x23, 0xed, 0x90, 0x6e, 0x50, 0x00,

                0x99, 0x9e, 0x4d, 0xd9, 0xda, 0x8d, 0x6f, 0x5f, 0x3e, 0xd7, 0x21, 0x74, 0x86, 0xdf, 0x6b, 0x05,

                0x8e, 0x5d, 0x37, 0x11, 0xd2, 0x28, 0x75, 0xd6, 0xa7, 0x77, 0x24, 0xbf, 0xf0, 0xb0, 0x02, 0xb7,

                0xf8, 0xfc, 0x81, 0x09, 0xb1, 0x01, 0x76, 0x91, 0x7d, 0x0f, 0xc8, 0xa0, 0xf2, 0xcb, 0x78, 0x60,

                0xd1, 0xf7, 0xe0, 0xb5, 0x98, 0x22, 0xb3, 0x20, 0x1d, 0xa6, 0xdb, 0x7b, 0x59, 0x9f, 0xae, 0x31,

                0xfb, 0xd3, 0xb6, 0xca, 0x43, 0x72, 0x07, 0xf4, 0xd8, 0x41, 0x14, 0x55, 0x0d, 0x54, 0x8b, 0xb9,

                0xad, 0x46, 0x0b, 0xaf, 0x80, 0x52, 0x2c, 0xfa, 0x8c, 0x89, 0x66, 0xfd, 0xb2, 0xa9, 0x9b, 0xc0]
    
    Permutation = [1,7,5,4,2,6,0,3]
    def __init__(self,CommonKey, data):
        self.CommonKey = CommonKey
        self.KEY =  []
        self.DATA = data
        self.KeySchedule()
        
    def KeySchedule (self):
        
        self.KEY = self.CommonKey #ici les 64 premiers bit de la clé sur les ...
        for i in range(1,7):
            keyTemp = self.KEY[64*(i-1):64*i]
            keyProv = []
            #permutation
            for j in range(len(keyTemp)):
            
                keyProv.append(keyTemp[self.KeyBitPermutation[j]])
           
            self.KEY = self.KEY + self.XORTOLIST(keyProv, i)
        self.KEYINT = self.listToInt(self.KEY)
    def XORTOLIST(self, li,i):
        for j in range (len(li)):
            li[j] = li[j] ^ self.XOR[i-1][j%8]
        return li
    def listToInt(self, li):
        li2 =[]
        
        for i in range (int((len(li)/8))):
            out = 0
            for bit in li[i*8:i*8+8]:
                out = (out << 1) | bit
            li2.append(out)

        return li2
    def permutaionBit(self, value):
        string = bin(value)[2:]
        string = '0'*(8-len(string)) + string
       
        reponse=""
        for i in range(7):
            reponse += string[self.Permutation[i]]
        
        return int('0b'+reponse,2)
    def roundFunction(self, tour = 56):
        for n in  range (tour):
          
            data = []
            x = self.BlockSBOX[self.KEYINT[n] ^self.DATA[7]]
            y = self.permutaionBit(x)
            data.append(self.DATA[1])
            data.append(self.DATA[2] ^ self.DATA[0])
            data.append(self.DATA[3] ^ self.DATA[0])
            data.append(self.DATA[4] ^ self.DATA[0])
            data.append(self.DATA[5])
            data.append(self.DATA[6] ^y)
            data.append(self.DATA[7])
            data.append(self.DATA[0] ^x)
            self.DATA = data
    def decription(self, tour = 56):
        for n in  range (tour):
          
            data = []
            x = self.BlockSBOX[self.KEYINT[tour-1-n] ^self.DATA[6]]
            y = self.permutaionBit(x)
            data.append(self.DATA[7] ^ x)
            data.append(self.DATA[0] )
            data.append(self.DATA[7] ^ self.DATA[1] ^x)
            data.append(self.DATA[7] ^ self.DATA[2] ^x)
            data.append(self.DATA[7] ^ self.DATA[3] ^x)
            data.append(self.DATA[4])
            data.append(self.DATA[5] ^y)
            data.append(self.DATA[6])
            self.DATA = data
"""
key =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
block = BlockCipher(key,  [1,2,3,4,5,6,7,8])        

block.roundFunction(56)
print (block.DATA)
block.decription(56)
print (block.DATA)"""