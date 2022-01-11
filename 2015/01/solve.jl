debug = false
filename = if debug "test.txt" else "input.txt" end

line = open(filename) do f
    read(f, String) |> strip
end

# Part 1
println("Part 1")
println(count('(', line) - count(')', line))

# Part 2
changes = [if c == '(' 1 else -1 end for c in line]
diff = cumsum(changes)
index = findfirst(==(-1), diff)

println("Part 2")
println(index)