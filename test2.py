

class BucketList:
	buckets = []

	## attempts to insert item into the first bucket for which
	## matchFunc(item, bucket) returns True
	## if checkUnique, assert that item only matches one or zero buckets
	## TODO: what to do if multiple match? maybe return generator in all cases
	def insert(self, item, matchFunc, checkUnique = True):
		gen = (b for b in self.buckets if matchFunc(item, b))
		bucket = next(gen, None)
		if checkUnique: assert next(gen, None) == None, 'item matched more than one bucket'
		bucket.append(item) if bucket else self.buckets.append([item])




bl = BucketList()

matchFunc = lambda item, bucket: bucket[0].startswith(item)# or item.startswith(bucket[0])
bl.insert('foo', matchFunc)
bl.insert('foo123', matchFunc)
bl.insert('cat', matchFunc)

try:
	bl.insert('fo', matchFunc)
except AssertionError:
	print('warning: multiple match')
	bl.insert('fo', matchFunc, checkUnique = False)

print(bl.buckets)