debug = false
filename = if debug "test.txt" else "input.txt" end

operations = Dict(
    "AND" => &,
    "OR" => |,
    "LSHIFT" => <<,
    "RSHIFT" => >>,
)

instructions = [
    [part for part in split(line) if part != "->"]
    for line in readlines(filename)
]

function emulate(instructions)
    wires = Dict{String, UInt16}()
    queue = copy(instructions)

    function check!(instruction, inputs)
        for input in inputs
            if tryparse(Int, input) === nothing && (!haskey(wires, input))
                push!(queue, instruction)
                return false
            end
        end
        true
    end

    function value(signal)
        try
            return parse(UInt16, signal)
        catch
            return wires[signal]
        end
    end

    while length(queue) > 0
        instruction = popfirst!(queue)

        if length(instruction) == 2
            signal, outwire = instruction
            if check!(instruction, [signal])
                wires[outwire] = value(signal)
            end
        elseif length(instruction) == 3
            _, inwire, outwire = instruction
            if check!(instruction, [inwire])
                wires[outwire] = ~value(inwire)
            end
        elseif length(instruction) == 4
            inwire1, operation, inwire2, outwire = instruction
            if check!(instruction, [inwire1, inwire2])
                wires[outwire] = operations[operation](value(inwire1), value(inwire2))
            end
        end
    end

    return wires
end

println("Part 1")
wires = emulate(instructions)
# println(wires)
println(Int(wires["a"]))

println("Part 2")
instructions = [instruction for instruction in instructions if instruction[end] != "b"]
push!(instructions, [string(wires["a"]), "b"])
new_wires = emulate(instructions)
print(new_wires["a"])