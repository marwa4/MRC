import numpy as np
import matplotlib.pyplot as plt
import numpy.random as nr

blockLength = 10000 # Number of symbol per block
nBlocks = 1000 # Number of blocks
Nr = 2 # 2 Receive antennas
SNRdB = np.arange(1.0,20.0,1.5) # SNR range in dB
BER = np.zeros(len(SNRdB))
BERt = np.zeros(len(SNRdB))
SNR = 10**(SNRdB/10) # Linear SNR

for blk in range(nBlocks):
    h=(nr.normal(0.0,1.0,(Nr,blockLength))+1j*nr.normal(0.0,1.0,(Nr,blockLength)))/np.sqrt(2) # Fading channel coefficient
    noise=nr.normal(0.0,1.0,(Nr,blockLength))+1j*nr.normal(0.0,1.0,(Nr,blockLength)) # AWGN
    Sym=2*nr.randint(2,size=blockLength)-1 # BPSK symbols
    for K in range(len(SNRdB)):
        TxBits = np.sqrt(SNR[K])*Sym
        RxBits=h*TxBits+noise # Channel effects ( Fading + AWGN )
        MRCout=np.sum(np.conj(h)*RxBits,axis=0) # Maximal Ratio combiner
        DecBits=2*(np.real(MRCout)>0)-1
        BER[K]=BER[K]+np.sum(DecBits!=Sym)


BER = BER/blockLength/nBlocks # Calculate the BER
lam = np.sqrt(SNR/(2+SNR))
BERt = 1/4*(1-lam)**2 * (2 + lam) # Theoretical BER
BERa = 3/4/SNR**2 # Approximation at high SNR
plt.yscale('log')
plt.plot(SNRdB, BER,'g-')
plt.plot(SNRdB, BERt,'ro')
plt.plot(SNRdB, BERa,'bs')
plt.grid(1,which='both')
plt.suptitle('BER for MRC')
plt.legend(["Simulation", "Theory","Approx"], loc ="lower left")
plt.xlabel('SNR (dB)')
plt.ylabel('BER') 
plt.savefig('BER for MRC.png', dpi = 300)