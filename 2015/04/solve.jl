using MD5

debug = false
filename = if debug "test.txt" else "input.txt" end

start = read(open(filename), String) |> strip

function searcher(zeros, start)
    i = 0
    target = repeat('0', zeros)
    while true
        i += 1
        hash = (start * string(i)) |> md5 |> bytes2hex
        if startswith(hash, target)
            return i
        end
    end
end

# Part 1
println("Part 1")
println(searcher(5, start))

# Part 2
println("Part 2")
println(searcher(6, start))
