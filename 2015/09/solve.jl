debug = false
filename = if debug "test.txt" else "input.txt" end

graph = Dict{Tuple{String, String}, Int}()

pattern = r"(.*) to (.*) = (.*)"
nodes = Set()

function order(a, b)
    if a < b
        return a, b
    else
        return b, a
    end
end

for line in readlines(filename)
    fromcity, tocity, distance_str = match(pattern, line)
    distance = parse(Int, distance_str)

    push!(nodes, fromcity)
    push!(nodes, tocity)

    graph[order(fromcity, tocity)] = distance
end

function path_length(graph, path)
    if length(path) == 1
        return 0
    end

    return sum(graph[order(edge...)] for edge in zip(path, path[2:end]))
end

function path_finder(graph, path_so_far, agg)
    remaining_nodes = setdiff(nodes, path_so_far)

    if length(remaining_nodes) == 0
        return path_length(graph, path_so_far)
    end

    return agg(
        path_finder(graph, [path_so_far; node], agg) 
        for node in remaining_nodes
    )
end

println("Part 1")
println(path_finder(graph, [], minimum))

println("Part 2")
println(path_finder(graph, [], maximum))