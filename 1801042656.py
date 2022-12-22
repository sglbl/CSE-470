# Suleyman Golbol 1801042656
# python 1801042656.py


class Sparkle:
    def reduncancy_remover(self, string):
        new_string = string & bin(11111111111111111111111111111111)
        return new_string

    def set_offset(self, offset):
        return offset % 32

    def rotator(self, offset, string):
        right_shifted = string >> self.set_offset(offset)
        left_shifted = string << (32 - self.set_offset(offset))
        ored = right_shifted | left_shifted
        return self.reduncancy_remover(ored)


    def from_array_converter(self, array):
        converted = bin(00000000000000000000000000000000)
        for i in range(len(array)):
            converted = converted << 32
            converted = converted | array[i]
        return converted


    
    def lfunction(self, string):
        rotated_16 = self.rotator(16, string)
        anded = string & bin(11111111111111111111111111111111)
        l_x = rotated_16 ^ anded
        return l_x

    def orer_for_converter(self, string):
        anded = string & ~bin(11111111111111111111111111111111)
        xored = string ^ anded
        return xored


    def to_array_converter(self, string, size):
        array = []
        counter = 0
        
        while(True):
            xored = self.orer_for_converter(string)
            array.append(xored)
            string = string >> 32    
            counter = counter + 1
            if counter == size-1:
                break
        array.reverse()
        return array
    
    
    def sequence_summer(self, array, index):
        return array[index] + array[index+1]
    
    def alzette_arx_box(self, array, key):
        for i in range(0,12):
            if i % 2 != 0: # apply this algorithm only for even indexes
                continue
            else:
                # self.reduncancy_remover = remove_excess
                rc = key[i>>1] # rc = round constant
                
                added_rotation = array[i] + self.rotator(31, array[i+1])
                array[i] = self.reduncancy_remover(added_rotation)  
                array[i+1] = array[i+1] ^ self.rotator(24, array[i])
                array[i] = array[i] ^ rc
                
                added_rotation = array[i] + self.rotator(17, array[i+1])
                array[i] = self.reduncancy_remover(added_rotation)
                array[i+1] = array[i+1] ^ self.rotator(17, array[i])
                array[i] = array[i] ^ rc

                added_sequence = self.sequence_summer(array, i)
                array[i] = self.reduncancy_remover(added_sequence)
                array[i+1] = array[i+1] ^ self.rotator(31, array[i])
                array[i] = array[i] ^ rc

                added_rotation = array[i] + self.rotator(24, array[i+1])
                array[i] = self.reduncancy_remover(added_rotation)
                array[i+1] = array[i+1] ^ self.rotator(16, array[i])
                array[i] = array[i] ^ rc
                
                
            
                
        
        
    
    def encoder(self, data_to_encrypt, key):
        # this code encrypts data with the 256bits key 

        array = self.to_array_converter(data_to_encrypt, 12)
        key_array = self.to_array_converter(key, 8)
        # 12 comes because the data is 384 bits and 384/32 = 12
        # 8 comes because the key is 256 bits and 256/32 = 8
        
        # ALZETTE DEPENDS ON 32 BIT CHUNKS ARX BOX
        
        for round_num, round_key in enumerate(key_array):
            array[1] = array[1] ^ round_key
            array[3] = array[3] ^ round_num

            for j in range(0, 12, 2):
                rc = key_array[j>>1]