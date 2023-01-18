# Suleyman Golbol 1801042656
# python 1801042656.py


from genericpath import getsize


class Sparkle:
    def reduncancy_remover(self, string):
        new_string = string & 0b11111111111111111111111111111111
        return new_string

    def set_offset(self, offset):
        return offset % 32

    def rotator(self, offset, string):
        right_shifted = string >> self.set_offset(offset)
        left_shifted = string << (32 - self.set_offset(offset))
        ored = right_shifted | left_shifted
        return self.reduncancy_remover(ored)


    def from_array_converter(self, array):
        # converted = 0b00000000000000000000000000000000
        converted = 0x0
        for i in range(len(array)):
            converted = converted << 32
            converted = converted | array[i]
        return converted
    
    def lfunction(self, string):
        rotated_16 = self.rotator(16, string)
        anded = string & 0b1111111111111111
        l_x = rotated_16 ^ anded
        return l_x

    def orer_for_converter(self, string):
        anded = string & (~0b11111111111111111111111111111111)
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
            if counter == size:
                break
        array.reverse()
        return array
    
    
    def sequence_summer(self, array, index):
        return array[index] + array[index+1]
    
    def alzette_arx_box_enc(self, array, key):
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
                
        return array
            
    def linear_diffusion_enc(self, array):
        temp1 = array[0]
        temp2 = array[1]
        
        x = array[0]
        y = array[1]
        
        for i in range(2,6):
            if i % 2 != 0:
                continue
            else:
                temp1 = temp1 ^ array[i]
                temp2 = temp2 ^ array[i+1]
                
        temp1 = self.lfunction(temp1)
        temp2 = self.lfunction(temp2)
        
        for i in range(2,6):
            if i % 2 != 0:
                continue
            else:
                array[i-2] = array[i+6] ^ array[i] ^ temp2
                array[i-1] = array[i+7] ^ array[i+1] ^ temp1
                array[i+6] = array[i]              
                array[i+7] = array[i+1]
        
        xored1 = x ^ temp2
        xored2 = y ^ temp1
        array[4] = array[6] ^ xored1
        array[5] = array[7] ^ xored2
        array[7] = y
        array[6] = x
        
        return array                    
        
    def encoder(self, data_to_encrypt, key):
        # this code encrypts data with the 256bits key 
        if key == None:
            # print("Key is not given")
            key = 0x432646294A404E635266556A586E3272357538782F413F4428472D4B61506453
        
        array = self.to_array_converter(data_to_encrypt, 12)
        
        key_array = self.to_array_converter(key, 8)
        # 12 comes because the data is 384 bits and 384/32 = 12
        # 8 comes because the key is 256 bits and 256/32 = 8
        
        # ALZETTE DEPENDS ON 32 BIT CHUNKS ARX BOX
        
        for round_num, round_key in enumerate(key_array):
            array[1] = array[1] ^ round_key
            array[3] = array[3] ^ round_num

            # Alzette
            array = self.alzette_arx_box_enc(array, key_array)
            # Linear diffusion
            array = self.linear_diffusion_enc(array)
        
        encrypted = self.from_array_converter(array)
        return encrypted
    
    
    #### DECODER ####
    
    def alzette_arx_box_dec(self, array, key): 
        for i in range(0,12):
            if i % 2 != 0:          
                continue
            else:
                rc = key[i>>1]
                
                array[i] = array[i] ^ rc
                rotated1 = self.rotator(16, array[i])
                array[i+1] = array[i+1] ^ rotated1
                rotated2 = self.rotator(24, array[i+1])
                array[i] = self.reduncancy_remover(array[i] - rotated2)
            
                array[i] = array[i] ^ rc
                rotated1 = self.rotator(31, array[i])
                array[i+1] = array[i+1] ^ rotated1
                array[i] = self.reduncancy_remover(array[i] - array[i+1])
                
                array[i] = array[i] ^ rc
                rotated1 = self.rotator(17, array[i])
                array[i+1] = array[i+1] ^ rotated1
                rotated2 = self.rotator(17, array[i+1])
                array[i] = self.reduncancy_remover(array[i] - rotated2)
                
                array[i] = array[i] ^ rc
                rotated1 = self.rotator(24, array[i])
                array[i+1] = array[i+1] ^ rotated1
                rotated2 = self.rotator(31, array[i+1])
                array[i] = self.reduncancy_remover(array[i] - rotated2)
                
        return array
                
            
    
    def linear_diffusion_dec(self, array):
        temp1 = 0
        temp2 = 0
        
        x = array[4]
        y = array[5]
        
        for i in reversed(range(1,5)):
            if i % 2 != 0:
                continue
            else:
                array[i] = array[i+6]
                temp1 = temp1 ^ array[i]
                array[i+6] = array[i-2]
                array[i+1] = array[i+7]
                temp2 = temp2 ^ array[i+1]
                array[i+7] = array[i-1]

        array[0] = array[6]
        temp1 = temp1 ^ array[6]
        array[6] = x
        
        array[1] = array[7]
        temp2 = temp2 ^ array[7]
        array[7] = y
        
        temp2 = self.lfunction(temp2)
        temp1 = self.lfunction(temp1)
        
        for i in reversed(range(0,5)):
            if i % 2 != 0:
                continue
            else:
                array[i+6] = array[i+6] ^ (array[i] ^ temp2)
                array[i+7] = array[i+7] ^ (array[i+1] ^ temp1)
        
        return array       
            
    
    def decoder(self, data_to_decrypt, key):
        # this code decrypts data with the 256bits key 
        
        array = self.to_array_converter(data_to_decrypt, 12)
        if key == None:
            # print("Key is not given")
            key = 0x432646294A404E635266556A586E3272357538782F413F4428472D4B61506453
        
        key_array = self.to_array_converter(key, 8)
        # 12 comes because the data is 384 bits and 384/32 = 12
        # 8 comes because the key is 256 bits and 256/32 = 8
        
        # ALZETTE DEPENDS ON 32 BIT CHUNKS ARX BOX
        length = len(key_array)
        for i in reversed(range(0, length)):
            # Linear diffusion
            array = self.linear_diffusion_dec(array)
            # Alzette
            array = self.alzette_arx_box_dec(array, key_array)

            array[1] = array[1] ^ key_array[i]
            array[3] = array[3] ^ i
               
        
        decrypted = self.from_array_converter(array)
        return decrypted

########## END OF CLASS #########

def ecb_mode_encoding(chunks, algorithm, key):
    encrypted_chunks = []
    for chunk in chunks:
        # encoded = algorithm.encoder(chunk, key)
        encoded = algorithm(chunk, key)
        encrypted_chunks.append(encoded)
    return encrypted_chunks
    
def cbc(chunks, algorithm, key, is_decoding=True):
    initialization_vector = 0x59161abcdef16195
    handled_chunks = []
    if is_decoding == False:  # Encoding
        for chunk in chunks:
            chunk = chunk ^ initialization_vector # XOR with IV
            decoded = algorithm(chunk, key)
            handled_chunks.append(decoded)
            initialization_vector = handled_chunks[-1] # -1 is the last element
    else:   # Decoding
        for chunk in chunks:
            chunk = chunk ^ initialization_vector # XOR with IV
            encoded = algorithm(chunk, key)
            handled_chunks.append(encoded)
            handled_chunks[-1] = handled_chunks[-1] ^ initialization_vector # XOR with IV
    
    return handled_chunks

def cfb(chunks, algorithm, key, is_decoding=True):
    initialization_vector = 0x59161abcdef16195
    handled_chunks = []
    if is_decoding == False:  # Encoding
        for i in range(len(chunks)):
            encoded = algorithm(initialization_vector, key)
            handled_chunks.append(encoded)
            handled_chunks[len(handled_chunks)-1] = handled_chunks[len(handled_chunks)-1] ^ chunks[i]
            initialization_vector = handled_chunks[len(handled_chunks)-1]   
    else:  # Decoding
        for i in range(len(chunks)):
            encoded = algorithm(initialization_vector, key)
            handled_chunks.append(encoded)
            handled_chunks[len(handled_chunks)-1] = handled_chunks[len(handled_chunks)-1] ^ chunks[i]
            initialization_vector = chunks[i]
    
    return handled_chunks

def ofb(chunks, algorithm, key, is_decoding=True):
    initialization_vector = 0x59161abcdef16195
    handled_chunks = []
    if is_decoding == False or is_decoding == True:  # Doesn't matter
        for i in range(len(chunks)):
            encoded = algorithm(initialization_vector, key)
            handled_chunks.append(encoded)
            initialization_vector = handled_chunks[len(handled_chunks)-1]   
            handled_chunks[len(handled_chunks)-1] = handled_chunks[len(handled_chunks)-1] ^ chunks[i]
    return handled_chunks

def read_as_bytes(block_length, file_path, ignore_last=False):
    readed = []

    with open(file_path, 'rb') as file:
        block = file.read(block_length)
        while block is not None and block != b'':
            integer_represented = int.from_bytes(block, byteorder='big')
            readed.append(integer_represented)
            block = file.read(block_length)
    
    if ignore_last==True:
        readed = readed[:len(readed)-1]
        if getsize(file_path) % block_length == 0:
            pass
        else:
            last_block = readed[-1]
            readed[-1] = last_block >> ((block_length - (getsize(file_path) % block_length)) * 8)
        
    if getsize(file_path) % block_length == 0:
        pass # no problem
    else:
        # Padding 
        # print("The file is not a multiple of 48 bytes so the last block will be padded with zeros")
        last_block = readed[-1]
        last_block = last_block << (block_length - (getsize(file_path) % block_length)) * 8
        pad = []
        if (getsize(file_path) % block_length) + 1 < block_length:
            last_block = last_block ^ (block_length - (getsize(file_path) % block_length))
        pad.append(last_block)
        if (getsize(file_path) % block_length) + 1 >= block_length:
            pad.append(-(getsize(file_path) % block_length) + block_length * 2)
        readed = readed[:len(readed)-1] + pad
    return readed

def write_as_bytes(chunks, needs_unpadding, file_path):
    pad = 0
    if needs_unpadding == True:
        # Unpadding because of the padding
        # chunks[len(chunks)-1] & 0b11111111 is checksum
        if (chunks[len(chunks)-1] & 0b11111111) < 2:
            pad = 0
        elif (chunks[len(chunks)-1] & 0b11111111) > 49:
            pad = 0
        elif (chunks[len(chunks)-1] & 0b11111111) == 49:
            if (chunks[len(chunks)-2] & 0b11111111) == 0\
            and (chunks[len(chunks)-1] & 0b11111111) == 49:
                chunks = chunks[:-1]
                pad = 1
            else: 
                pad = 0
        # check if the last byte is a padding byte using the mask 2 ** (8 * (last_byte & 0b11111111)) - 1
        elif (chunks[len(chunks)-1] & (2**(8 * (chunks[len(chunks)-1] & 0b11111111))-1)) == (chunks[len(chunks)-1] & 0b11111111):
            pad = chunks[len(chunks)-1] & 0b11111111
        else:
            pad = 0
    with open(file_path, 'wb') as file:
        block_length = 48
        for chunk in chunks:
            if needs_unpadding == True:
                if chunk is chunks[len(chunks)-1]: # last chunk
                    block_length = block_length - pad
                    chunk >>=  pad * 8
            to_write = chunk.to_bytes(block_length, byteorder='big')
            file.write(to_write)

# Taking input from user properly
def take_input(string, int_type=False):
    wrong_input = True
    while wrong_input == True:
        try:
            inp_value = input(string)
            if int_type == True and inp_value.isdigit() == False:
                raise TypeError 
            wrong_input = False
        # value or type error
        except ValueError:
            print("Wrong input. Please try again.")
        except TypeError:
            print("Wrong input. Please try again.")
    return inp_value    
  
def get_output_by_mode(mode, input_blocks, sparkle, is_encoder=True):
    if is_encoder == True:
        if mode == "2":
            output = ofb(input_blocks, sparkle.encoder, key=None)
        elif mode == "3":
            output = cfb(input_blocks, sparkle.encoder, key=None)
        elif mode == "4":
            output = cbc(input_blocks, sparkle.encoder, key=None)
        else:        
            output = ecb_mode_encoding(input_blocks, sparkle.encoder, key=None)
    else: # is_encoder == False
        if mode == "2":
            output = ofb(input_blocks, sparkle.decoder, key=None)
        elif mode == "3":
            output = cfb(input_blocks, sparkle.decoder, key=None)
        elif mode == "4":
            output = cbc(input_blocks, sparkle.decoder, key=None)
        else:        
            output = ecb_mode_encoding(input_blocks, sparkle.decoder, key=None)    
    return output           
  
  
def menu():
    sparkle = Sparkle()
    print("Welcome to the Suleyman's Cryptography program.")
    print("Press 1 to encrypt file using key file\
        \nPress 2 to decrypt file using key file\
        \nPress 3 to check changes using mode as hash\
        \nPress 4 to sign input with key into output\
        \nPress 5 to validate integrity\
        \nPress 6 to generate hash of input to output")
    input = take_input("Enter input: ", int_type=True)
    
    if input != "3":
        input_file = take_input("Enter the input file path: ")
        key = take_input("Enter the key file path: ")
        if input != "5":
            output_file = take_input("Enter the output file path: ")        
        mode = take_input("Select mode: 1 for ECB, 2 for OFB, 3 for CFB, 4 for CBC: ", int_type=True)
        
    if input == "1":
        input_blocks = read_as_bytes(block_length=48, file_path=input_file)
        key = read_as_bytes(block_length=32, file_path=key)[0]
        out = get_output_by_mode(mode, input_blocks, sparkle, is_encoder=True)
        write_as_bytes(out, needs_unpadding=False, file_path=output_file)
        print("\nDone encrypting.")
        
    elif input == "2":
        input_blocks = read_as_bytes(block_length=48, file_path=input_file)
        key = read_as_bytes(block_length=32, file_path=key)[0]
        out = get_output_by_mode(mode, input_blocks, sparkle, is_encoder=False)
        write_as_bytes(out, needs_unpadding=True, file_path=output_file)
        print("\nDone decrypting.")
    
    elif input == "3":
        mode = take_input("Select mode: 1 for ECB, 2 for OFB, 3 for CFB, 4 for CBC: ", int_type=True)
        input1 = take_input("Enter the input file path: ")
        input2 = take_input("Enter the comparison file path: ")

        input_blocks = read_as_bytes(block_length=48, file_path=input1)
        compared = read_as_bytes(block_length=48, file_path=input2)
        
        output = get_output_by_mode(mode, input_blocks, sparkle, is_encoder=True)
        
        output = xor(output)
        if output[0] == compared[0]:
            print("Files are using same hash.")
        else:
            print("Files are using different hash.")

    elif input == "4":
        input_blocks = read_as_bytes(block_length=48, file_path=input_file)
        key = read_as_bytes(block_length=32, file_path=key)[0]
        if mode == "2":
            output = ofb(input_blocks, sparkle.encoder, key)
        elif mode == "3":
            output = cfb(input_blocks, sparkle.encoder, key)
        elif mode == "4":
            output = cbc(input_blocks, sparkle.encoder, key)   
        else:
            output = ecb_mode_encoding(input_blocks, sparkle.encoder, key)
        output = xor(output)
        with open(input_file, "wb") as f:
            f.write(output[0].to_bytes(48, byteorder='big'))
        print("Done writing/signing hash to file.")
        
    elif input == "5":
        input_blocks = read_as_bytes(block_length=48, file_path=input_file, ignore_last=True)
        key = read_as_bytes(block_length=32, file_path=key)[0]
        if mode == "2":
            output = ofb(input_blocks, sparkle.encoder, key)
        elif mode == "3":
            output = cfb(input_blocks, sparkle.encoder, key)
        elif mode == "4":
            output = cbc(input_blocks, sparkle.encoder, key)
        else:
            output = ecb_mode_encoding(input_blocks, sparkle.encoder, key)
        output = xor(output)
        try:
            with open(input_file, "wb") as f:
                f.seek(-48, 2)
                comp = int.from_bytes(f.read(48), byteorder='big')
        except:
            print("Integrity is valid.") # if file isn't signed, it's valid
            return
        if output[0] == comp:
            print("Integrity is valid.")
        else:
            print("Integrity is not valid.")
   
    elif input == "6":
        input_blocks = read_as_bytes(block_length=48, file_path=input_file)
        if mode == "2":
            output = ofb(input_blocks, sparkle.encoder, key=None)
        elif mode == "3":
            output = cfb(input_blocks, sparkle.encoder, key=None)
        elif mode == "4":
            output = cbc(input_blocks, sparkle.encoder, key=None)
        else:
            output = ecb_mode_encoding(input_blocks, sparkle.encoder, key=None)
        output = xor(output)
        write_as_bytes(output, needs_unpadding=False, file_path=output_file)
        print("Done generating hash to file. Result is: ", hex(output[0]))
   
def xor(blocks):
	out = 0x0
	for i in range(len(blocks)):
		out ^= blocks[i]
	return [out]     
    
  
if __name__ == "__main__": 
    menu()
    
    # sparkle = Sparkle()
    # input_blocks = read_as_bytes(block_length=48, file_path='derbashi-xoorkle/README.md')
    # key = read_as_bytes(block_length=32, file_path="BIL470-odev22.pdf")[0]
    # out = ecb_mode_encoding(input_blocks, sparkle.encoder, key)
    # write_as_bytes(out, needs_unpadding=False, file_path="derbashi-xoorkle/output")
    # print("\nDone encrypting.")
    
    # input_blocks = read_as_bytes(block_length=48, file_path="derbashi-xoorkle/output")
    # key = read_as_bytes(block_length=32, file_path="BIL470-odev22.pdf")[0]
    # out = ecb_mode_encoding(input_blocks, sparkle.decoder, key)
    # write_as_bytes(out, needs_unpadding=True, file_path="sgl.txt")
    # print("\nDone decrypting")
