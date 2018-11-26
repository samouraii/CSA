from KeySchedule import *

class StreamCipher:
    #key est une keyshedule

    sbox = [[(1,0),(1,1),(1,0),(1,1),(1,0),(0,0),(0,0)],#0
            [(0,0),(0,1),(0,0),(0,1),(0,0),(0,1),(1,1)],
            [(0,1),(0,0),(0,1),(1,0),(0,0),(1,0),(1,0)],
            [(0,1),(1,0),(1,0),(1,1),(0,1),(1,1),(1,0)],
            [(1,0),(1,0),(1,0),(0,0),(1,1),(0,1),(1,1)],
            [(1,1),(1,1),(1,1),(1,0),(1,0),(1,0),(0,0)],#5
            [(1,1),(1,1),(1,1),(0,1),(1,1),(1,0),(0,0)],
            [(0,0),(0,0),(0,1),(1,0),(1,0),(0,0),(0,1)],
            [(1,1),(0,1),(0,1),(0,1),(0,0),(0,0),(1,1)],
            [(1,0),(1,1),(0,1),(1,0),(0,1),(0,1),(0,0)],
            [(1,0),(1,0),(0,0),(0,0),(1,1),(1,1),(0,1)],#10
            [(0,0),(0,1),(1,1),(0,1),(1,1),(0,0),(1,1)],
            [(0,1),(0,0),(1,1),(1,1),(0,1),(1,0),(0,1)],
            [(0,1),(0,0),(0,0),(0,0),(0,0),(1,1),(1,0)],
            [(0,0),(0,1),(1,0),(0,0),(1,0),(0,1),(1,0)],
            [(1,1),(1,0),(0,0),(1,1),(0,1),(1,1),(0,1)],#15
            [(0,0),(1,1),(0,1),(0,1),(1,0),(1,0),(0,1)],
            [(1,1),(0,1),(1,1),(0,0),(1,1),(1,1),(0,0)],
            [(1,1),(0,0),(0,0),(1,1),(1,0),(0,0),(1,1)],
            [(0,0),(1,1),(0,1),(0,1),(0,0),(1,0),(1,1)],
            [(1,0),(1,1),(1,1),(1,0),(0,0),(1,1),(0,0)],#20
            [(1,0),(1,0),(0,0),(1,1),(1,1),(0,0),(0,1)],
            [(0,1),(0,0),(1,0),(0,0),(0,1),(0,1),(0,1)],
            [(0,1),(1,0),(1,0),(1,1),(0,1),(0,1),(1,0)],
            [(1,0),(0,0),(1,0),(0,0),(0,1),(1,0),(1,0)],
            [(1,0),(0,0),(0,0),(1,1),(0,0),(0,1),(1,1)],#19
            [(0,0),(0,1),(0,1),(1,0),(1,1),(0,1),(0,1)],
            [(1,1),(1,0),(1,0),(0,0),(1,0),(1,0),(0,0)],
            [(0,1),(1,0),(0,0),(0,1),(1,1),(0,0),(1,0)],
            [(0,1),(0,1),(1,1),(1,0),(0,1),(1,1),(1,1)],
            [(1,1),(1,1),(1,1),(1,0),(0,0),(1,1),(0,0)],
            [(0,0),(0,1),(0,1),(0,1),(1,0),(0,0),(1,0)],
            ]
    
    def __init__(self, key, data) :
        self.KEY = key
        self.DATA = data
        self.registerA = [0b0000] *10
        self.registerB = [0b0000]*10
        self.registerX = 0
        self.registerY = 0
        self.registerZ = 0
        self.registerE = 0
        self.registerF = 0
        self.registerP = 0
        self.registerQ = 0
        self.registerC = 0
        self.D = 0
        self.Mode = 0 # 0 init 1 mode generation
        self.result = []

        self.registerA = self.registerA
        self.loadKey()
        self.tourInitialisation()
    def addValueRegister(self,register, value):
        register = [value] + register
        del register[len(register) -1]
        return register
    def loadKey(self):
        for i in range(0,8):
            self.registerA[i] = int('0b'+str(self.KEY[i*4]) +str(self.KEY[i*4+1]) +str(self.KEY[i*4+2])+str(self.KEY[i*4+3]),2)
            self.registerB[i] = int('0b'+str(self.KEY[32+i*4]) +str(self.KEY[32+i*4+1]) +str(self.KEY[32+i*4+2])+str(self.KEY[32+i*4+3]),2)
    def rounds(self, data):
        self.DATA = data
        self.tourInitialisation()
    def tourInitialisation(self):
        
        self.result = []
        IA = 0
        IB = 0
        i = 0 
        for ti in range(-32+1,0+1):
            if ti % 2 == 1:
                
                IA = self.DATA[i]  // (2**4)
                IB = self.DATA[i]  % (2**4)
            else:
                IA = self.DATA[i] % (2**4)
                IB = self.DATA[i]  // (2**4)
            if ti %4 == 0:
                i+=1
            if self.Mode == 0 :    
                aPrime = self.registerA[9] ^ self.registerX ^ self.D ^ IA
                bPrime = self.registerB[6] ^self.registerA[9] ^self.registerY ^IB
            if self.Mode == 1:
                aPrime = self.registerA[9] ^ self.registerX
                bPrime = self.registerB[6] ^self.registerA[9] ^self.registerY
            if self.registerP == 1:
                bPrime = StreamCipher.rol(bPrime)
            self.generation() 
            self.registerA =self.addValueRegister(self.registerA, aPrime)
            self.registerB = self.addValueRegister(self.registerB, bPrime)
        self.Mode = 1
        return IA
    def generation(self):
        ePrime = self.registerE
        fPrime = self.registerF
        cPrime = self.registerC
        if self.registerQ != 0:
            ePrime = self.registerF
            fPrime = self.registerF | self.registerZ | (self.registerC % (2**4))
        else:
            if (self.registerE | self.registerZ | self.registerC) < (2**4):
                cPrime = 0
            else:
                cPrime = 1
        dPrime = self.registerE ^self.registerZ ^ self.Bout()
        self.inbox()
        if self.Mode == 1:
            self.result.append(self.bitToInt(dPrime, 2) ^self.bitToInt(dPrime, 3))
            self.result.append(self.bitToInt(dPrime, 0) ^self.bitToInt(dPrime, 1))
        
        self.registerX = int('0b'+str(self.sbox[self.s4][3][0])+str(self.sbox[self.s3][2][0])+str(self.sbox[self.s2][1][1])+str(self.sbox[self.s1][0][1]),2)
        self.registerY = int('0b'+str(self.sbox[self.s6][5][0])+str(self.sbox[self.s5][4][0])+str(self.sbox[self.s4][3][1])+str(self.sbox[self.s3][2][1]),2)
        self.registerZ = int('0b'+str(self.sbox[self.s2][1][0])+str(self.sbox[self.s1][0][0])+str(self.sbox[self.s6][5][1])+str(self.sbox[self.s5][4][1]),2)
        self.registerP = int ('0b'+str(self.sbox[self.s7][6][1]),2)
        self.registerq = int ('0b'+str(self.sbox[self.s7][6][0]),2)

        self.registerE = ePrime
        self.registerF = fPrime
        self.registerc = cPrime
     
    def getResultInt(self):
        li2 =[]
        
        for i in range (int((len(self.result)/8))):
            out = 0
            for bit in self.result[i*8:i*8+8]:
                out = (out << 1) | bit
            li2.append(out)

        return li2
        
    def inbox (self):
        self.s1 = int(str(self.bitToInt(self.registerA[3],0))+str(self.bitToInt(self.registerA[0],2))+str(self.bitToInt(self.registerA[5],1))
                 + str(self.bitToInt(self.registerA[6],3))+str(self.bitToInt(self.registerA[8],0)),2)
        self.s2 = int(str(self.bitToInt(self.registerA[1],1))+str(self.bitToInt(self.registerA[2],2))+str(self.bitToInt(self.registerA[5],3))
                 + str(self.bitToInt(self.registerA[6],0))+str(self.bitToInt(self.registerA[8],1)),2)
        self.s3 = int(str(self.bitToInt(self.registerA[0],3))+str(self.bitToInt(self.registerA[1],0))+str(self.bitToInt(self.registerA[4],1))
                 + str(self.bitToInt(self.registerA[4],3))+str(self.bitToInt(self.registerA[5],2)),2)
        self.s4 = int(str(self.bitToInt(self.registerA[2],3))+str(self.bitToInt(self.registerA[0],1))+str(self.bitToInt(self.registerA[1],3))
                 + str(self.bitToInt(self.registerA[3],2))+str(self.bitToInt(self.registerA[7],0)),2)
        self.s5 = int(str(self.bitToInt(self.registerA[4],2))+str(self.bitToInt(self.registerA[3],3))+str(self.bitToInt(self.registerA[5],0))
                 + str(self.bitToInt(self.registerA[7],1))+str(self.bitToInt(self.registerA[8],2)),2)
        self.s6 = int(str(self.bitToInt(self.registerA[2],1))+str(self.bitToInt(self.registerA[3],1))+str(self.bitToInt(self.registerA[4],0))
                 + str(self.bitToInt(self.registerA[6],2))+str(self.bitToInt(self.registerA[8],3)),2)
        self.s7 = int(str(self.bitToInt(self.registerA[1],2))+str(self.bitToInt(self.registerA[2],0))+str(self.bitToInt(self.registerA[6],1))
                 + str(self.bitToInt(self.registerA[7],2))+str(self.bitToInt(self.registerA[7],3)),2)

  
    def bitToInt( self, value, pos):
        
        string = bin(value)[2:]
        string = '0'*(4-len(string)) + string
        return int(string[pos])
                
    def Bout (self):
        b3 = self.bitToInt(self.registerB[2],0) ^ self.bitToInt(self.registerB[5],1)^ self.bitToInt(self.registerB[6],2)^ self.bitToInt(self.registerB[8],3)
        b2 = self.bitToInt(self.registerB[5],0) ^ self.bitToInt(self.registerB[7],1)^ self.bitToInt(self.registerB[2],3)^ self.bitToInt(self.registerB[3],2)
        b1 = self.bitToInt(self.registerB[4],3) ^ self.bitToInt(self.registerB[7],2)^ self.bitToInt(self.registerB[3],0)^ self.bitToInt(self.registerB[4],1)
        b0 = self.bitToInt(self.registerB[8],2) ^ self.bitToInt(self.registerB[5],3)^ self.bitToInt(self.registerB[2],1)^ self.bitToInt(self.registerB[7],0)
        
        return int(str(b3)+str(b2)+str(b1)+str(b0))
    @staticmethod
    def rol(byte):
        return (byte << 1  | ((byte & 0b10000000) >> 7)) & 0xFF
"""
key = [0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
stream = StreamCipher(key, [1,2,3,4,5,6,7,8])
print (stream.registerA)
print (stream.registerB)
print (stream.tourInitialisation([1,2,3,4,5,6,7,8]))
print (stream.registerA)
stream.tourInitialisation([1,2,3,4,5,6,7,8])
print (stream.getResultInt())
stream.tourInitialisation([1,2,3,4,5,6,7,8])
print (stream.getResultInt())
"""
