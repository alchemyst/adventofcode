debug = false
filename = if debug "test.txt" else "input.txt" end

lines = readlines(filename)

function parse_input(lines)
    elf = []
    elves = [elf]
    
    for line in lines
        # Note if you don't use a function,
        # you have to add
        # global elf
        # global elves
        line = strip(line)
        if length(line) == 0
            elf = []
            push!(elves, elf) 
            continue
        end
    
        cals = parse(Int, line)
        push!(elf, cals)
    end

    return elves
end

elves = parse_input(lines)
sums = map(sum, elves)

println("Part 1")
println(maximum(sums))

println("Part 2")
top3 = partialsort!(sums, 1:3, rev=true)
println(sum(top3))