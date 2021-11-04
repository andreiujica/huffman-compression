
class Node:
    """Node class containing frequency of a symbol, left and right child and respective code(0/1)"""
    
    # A Huffman Tree Node
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.code = ''

def read_file(name, mode):
    """Generic function, reads data from a file"""

    with open(name, mode) as file:
        data = file.read()
    file.close()

    return data

def get_percentage(number1, number2):
    return round((1 - number1 / number2) * 100, 2) 

codes = dict()

def get_codes(node, val=''):
    """ A helper function to print the codes of symbols by traveling Huffman Tree"""

    # huffman code for current node
    newVal = val + str(node.code)

    if(node.left):
        get_codes(node.left, newVal)
    if(node.right):
        get_codes(node.right, newVal)

    if(not node.left and not node.right):
        codes[node.symbol] = newVal
         
    return codes        


def get_frequency(data):
    """ A helper function to calculate the probabilities of symbols in given data"""

    symbols = dict()
    for element in data:
        if symbols.get(element) == None:
            symbols[element] = 1
        else: 
            symbols[element] += 1     
    return symbols


def encode_output(data, coding):
    """ A helper function to obtain the encoded output"""

    encoding_output = []
    for c in data:
        encoding_output.append(coding[c])
        
    string = ''.join([str(item) for item in encoding_output])    
    return string

""" A helper function to calculate the space difference between compressed and non compressed data"""    
def Total_Gain(data, coding):
    before_compression = len(data) * 8 # total bit space to store the data before compression
    after_compression = 0
    symbols = coding.keys()
    for symbol in symbols:
        count = data.count(symbol)
        after_compression += count * len(coding[symbol]) #calculate how many bits are required for that symbol in total
    print(f"Space usage BEFORE compression: {before_compression} bits")    
    print(f"Space usage AFTER compression: {after_compression} bits")

    print(f"Reduction in space by: {get_percentage(after_compression, before_compression)} %")      

def Huffman_Encoding(data):
    """Main encoding function. Takes each symbol and converts it into a huff tree, then calculates codes
       based on the tree. Finally it replaces the text with the binary codes"""

    symbol_with_freq = get_frequency(data)
    symbols = symbol_with_freq.keys()
    frequencies = symbol_with_freq.values()
    print("symbols: ", symbols)
    print("frequencies: ", frequencies)
    
    nodes = []
    
    # converting symbols and probabilities into huffman tree nodes
    for symbol in symbols:
        nodes.append(Node(symbol_with_freq.get(symbol), symbol))
    
    while len(nodes) > 1:
        # sort all the nodes in ascending order based on their probability
        nodes = sorted(nodes, key=lambda x: x.freq)
        
        right = nodes[0]
        left = nodes[1]
    
        left.code = 0
        right.code = 1
    
        # combine the 2 smallest nodes to create new node
        newNode = Node(left.freq+right.freq, left.symbol+right.symbol, left, right)
    
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)
            
    huffman_encoding = get_codes(nodes[0])
    print("symbols with codes", huffman_encoding)
    Total_Gain(data, huffman_encoding)
    encoded_output = encode_output(data,huffman_encoding)
    return encoded_output, nodes[0]  
    
 
def Huffman_Decoding(encoded_data, huffman_tree):
    """Main decoding function. Walkx down the tree and unpacks it if it reaches the end"""

    tree_head = huffman_tree
    decoded_output = []
    for x in encoded_data:
        if x == '1':
            huffman_tree = huffman_tree.right   
        elif x == '0':
            huffman_tree = huffman_tree.left
        try:
            if huffman_tree.left.symbol == None and huffman_tree.right.symbol == None:
                pass
        except:
            decoded_output.append(huffman_tree.symbol)
            huffman_tree = tree_head
    
    # decoded output is a list and we are trying to get a string    
    string = ''.join([str(item) for item in decoded_output])
    return string        


def main():
    data = read_file("hobbit.txt", "r")
    encoding, tree = Huffman_Encoding(data)
    Huffman_Decoding(encoding, tree)

if __name__ == "__main__":
    main()