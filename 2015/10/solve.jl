using IterTools

debug = false
filename = if debug "test.txt" else "input.txt" end

line = readline(filename)

look_and_say(line) = join("$(length(group))$(group[1])" for group in groupby(identity, line))

look_and_say(line, n) = nth(iterated(look_and_say, line), n+1)

if debug
    examples = (
        "1" => "11",
        "11" => "21",
        "21" => "1211",
        "1211" => "111221",
        "111221" => "312211",
    )

    for (start, result) in examples
        @assert look_and_say(start) == result
    end
end

println("Part 1")
println(length(look_and_say(line, 40)))

println("Part 2")
println(length(look_and_say(line, 50)))