debug = false
filename = if debug "test.txt" else "input.txt" end

instruction_re = r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)"

instructions = open(filename) do f
    [match(instruction_re, line) for line in readlines(f)]
end

# Part 1
function part1()
    lights = zeros(Bool, (1000, 1000))
    for instruction in instructions
        action, coords... = instruction
        r1, c1, r2, c2 = parse.(Int, coords) .+ 1
        if action == "turn on"
            lights[r1:r2, c1:c2] .= true
        elseif action == "turn off"
            lights[r1:r2, c1:c2] .= false
        elseif action == "toggle"
            lights[r1:r2, c1:c2] .= .!lights[r1:r2, c1:c2]
        end
    end
    sum(lights)
end


println("Part 1")
println(part1())

# Part 2

function part2()
    lights = zeros(Int, (1000, 1000))
    for instruction in instructions
        action, coords... = instruction
        r1, c1, r2, c2 = parse.(Int, coords) .+ 1
        if action == "turn on"
            lights[r1:r2, c1:c2] .+= 1
        elseif action == "turn off"
            lights[r1:r2, c1:c2] .-= 1
        elseif action == "toggle"
            lights[r1:r2, c1:c2] .+= 2
        end
        lights[lights .< 0] .= 0
    end
    sum(lights)
end

println("Part 2")
println(part2())