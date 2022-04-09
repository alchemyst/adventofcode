debug = false
filename = if debug "test.txt" else "input.txt" end


data = []

f = open(filename)
for line in readlines(f)
    l, w, h = map(s -> parse(Int, s), split(line, 'x'))
    push!(data, [l, w, h])
end

return data

# Part 1
area = 0

for (l, w, h) in data
    sides = [l * w, w * h, h * l]
    global area += 2*sum(sides) + minimum(sides)
end

println("Part 1")
println(area)

ribbon_length = 0

for (l, w, h) in data
    volume = l * w * h
    smallest, second_smallest, biggest = sort([l, w, h])
    global ribbon_length += 2*(smallest + biggest) + volume
end

println("Part 2")
println(ribbon_length)