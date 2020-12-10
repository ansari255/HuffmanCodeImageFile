import numpy as pnum
import imageio
import queue

class Branch:
	def __init__(self):
		self.prob = None
		self.code = None
		self.data = None
		self.left = None
		self.right = None 	
	def __lt__(self, new):
		if (self.prob < new.prob):		
			return 1
		else:
			return 0
	def __ge__(self, new):
		if (self.prob > new.prob):
			return 1
		else:
			return 0
            
def color_to_grey(img):
	grey_img = pnum.rint(img[:,:,0]*0.2989 + img[:,:,1]*0.5870 + img[:,:,2]*0.1140)
	grey_img = grey_img.astype(int)
	return grey_img
    
def prob_tree(probs):
	priority_q = queue.PriorityQueue()
	for color,probability in enumerate(probs):
		twig = Branch()
		twig.data = color
		twig.prob = probability
		priority_q.put(twig)

	while (priority_q.qsize()>1):
		newbranch = Branch()		
		ls = priority_q.get()
		rs = priority_q.get()			
						
		newbranch.left = ls 		
		newbranch.right = rs
		newprob = ls.prob+rs.prob	
		newbranch.prob = newprob
		priority_q.put(newbranch)	
	return priority_q.get()		

def huffman_construct(root_branch,temp_array,f_code):		
	if (root_branch.left is not None):
		temp_array[huffman_construct.count] = 1
		huffman_construct.count+=1
		huffman_construct(root_branch.left,temp_array,f_code)
		huffman_construct.count-=1
	if (root_branch.right is not None):
		temp_array[huffman_construct.count] = 0
		huffman_construct.count+=1
		huffman_construct(root_branch.right,temp_array,f_code)
		huffman_construct.count-=1
	else:
		huffman_construct.output_bits[root_branch.data] = huffman_construct.count		
		color_code = ''.join(str(cell) for cell in temp_array[1:huffman_construct.count]) 
		color = str(root_branch.data)
		write_string = color+' '+ color_code+'\n'
		f_code.write(write_string)		
	return

img = imageio.imread('tulips.bmp')
grey_img = color_to_grey(img)

histog = pnum.bincount(grey_img.ravel(),minlength=256)
color_probs = histog/pnum.sum(histog)		
root_branch = prob_tree(color_probs)		

temp_array = pnum.ones([64],dtype=int)
huffman_construct.output_bits = pnum.empty(256,dtype=int) 
huffman_construct.count = 0
f_code = open('huffman_codes.txt','w')
huffman_construct(root_branch,temp_array,f_code)	

input_bits = img.shape[0]*img.shape[1]*8	
img_compression = (1-pnum.sum(huffman_construct.output_bits*histog)/input_bits)*100	
print('Compression of image is ',img_compression,' percent')