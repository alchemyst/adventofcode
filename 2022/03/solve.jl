debug = false
filename = if debug "test.txt" else "input.txt" end

lines = readlines(filename)

priority = Dict(c=>i for (i, c) = enumerate(cat('a':'z', 'A':'Z', dims=1)))

function score1(line)
    half = Int(length(line)/2)
    c1 = line[1:half]
    c2 = line[half+1:end]

    return intersect(c1, c2)[1]
end

function run(f, input)
    return sum(priority[f(element)] for element = input)
end

println("Part 1")
println(run(score1, lines))

score2(group) = intersect(group...)[1]

println("Part 2")
println(run(score2, Iterators.partition(lines, 3)))