debug = false
filename = if debug "test.txt" else "input.txt" end

instructions = strip(read(open(filename), String))

movements = Dict(
    '>' => complex(1, 0),
    '<' => complex(-1, 0),
    '^' => complex(0, -1),
    'v' => complex(0, 1),
)

function traverse(instructions, counts)
    location = complex(0, 0)
    for instruction in instructions
        location += movements[instruction]
        if !(location in keys(counts))
            counts[location] = 1
        else
            counts[location] += 1
        end
    end
end

# Part 1
counts = Dict()
traverse(instructions, counts)

println("Part 1")
println(length(counts))

# Part 2
counts = Dict()
traverse(instructions[1:2:end], counts)
traverse(instructions[2:2:end], counts)
println("Part 2")
println(length(counts)) 