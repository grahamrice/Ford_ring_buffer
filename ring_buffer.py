class ring_buffer:
	def __init__(self,max):
		self.max = max
		self.full = False
		self.data = []
		self.next_write = 0
		self.result_pos = -1

	def overwrite(self,new_data):
		for i in range(len(new_data)):
			if self.next_write >= self.max:
				self.next_write = 0
			self.data[self.next_write] = new_data[i]
			self.next_write += 1


	def append(self,new_data):
		if self.full == False:
			if len(self.data) + len(new_data) <= self.max:
				self.data.extend(new_data)
				self.next_write += len(new_data)
			else:
				len_to_extend = self.max - len(self.data)
				self.data.extend(new_data[:len_to_extend])
				self.next_write = 0
				self.overwrite(new_data[len_to_extend:])
				self.full = True
		else:
			self.overwrite(new_data)

	def get_list_back(self,start,length):
		if start - length >= 0: #we know we can safely take values backwards from start
			self.result_pos = start - length
			return self.data[(start-length):start]
		else:
			result = self.data[0:start]
			self.result_pos = self.max - length + start
			return self.data[start-length:] + result


	def search(self,match):
		if not match:
			return -1
		rest, last = match[:-1], match[len(match)-1]
		for m in range(self.next_write-1,-1,-1): #up to but not including -1
			if last == self.data[m]:
				if rest == self.get_list_back(m,len(rest)):
					return self.result_pos
		for n in range(self.max-1,self.next_write-1,-1):
			if last == self.data[n]:
				if rest == self.get_list_back(n,len(rest)):
					return self.result_pos
		return -1


if __name__ == '__main__':
	buffer = ring_buffer(0x10)
	temp = [1,2,3,4] * 5  #[1,2,3,4] * 3
	buffer.append(temp)
	print buffer.data
	print str(buffer.next_write)
	for j in range(10): #(10,20,1):
		buffer.append([j])
		print str(buffer.next_write)
		print buffer.data

	print "Found [7,8,9] at " + str(buffer.search([7,8,9]))
	print "Found [2,3,4] at " + str(buffer.search([2,3,4]))
