using Combinatorics

debug = false
filename = if debug "test.txt" else "input.txt" end

edgeweights = Dict()
nodes = Set()

function edge(a, b)
    if a < b
        (a, b)
    else
        (b, a)
    end 
end

for line in readlines(filename)
    a, _, sign, happiness, _, _, _, _, _, _, b = split(line[1:end-1])
    happiness = (sign == "gain" ? 1 : -1) * parse(Int, happiness)
    e = edge(a, b)
    edgeweights[e] = get(edgeweights, e, 0) + happiness

    push!(nodes, a)
    push!(nodes, b)
end

function pathhappiness(path)
    return sum(get(edgeweights, edge(e...), 0) for e in zip(path, path[2:end]))
end

function seat(first, rest)
    return maximum(
        pathhappiness([first; perm; first])
        for perm in permutations(rest)
    )
end

println("Part 1")
nodearray = [n for n in nodes]
println(seat(nodearray[1], nodearray[2:end]))

println("Part 2")
noone = "XXXXXXXX"
println(seat(noone, nodearray))