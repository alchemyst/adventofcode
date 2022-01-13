import numpy

a = numpy.array([int(line.strip()) for line in open('input.txt')])

# part 1.1

sum2 = a[:, None] + a[None, :]
match = numpy.nonzero(sum2 == 2020)
instance = match[0]
print(numpy.prod(a[instance]))

# part 1.2

sum3 = a[:, None, None] + a[None, :, None] + a[None, None, :]
match = numpy.nonzero(sum3 == 2020)
instance = [m[0] for m in match]
print(numpy.prod(a[instance]))
