debug = false
filename = if debug "test.txt" else "input.txt" end

lines = readlines(filename) .|> strip

countchars(func) = sum(length(func(line)) for line in lines)

parse_eval(line) = eval(Meta.parse(line))

# Part 1i
original_chars = countchars(identity)
memory_chars = countchars(parse_eval)

println("Part 1")
println(original_chars - memory_chars)

# Part 2

function escape(line)
    "\"" * replace(line, "\\" => "\\\\", "\"" => "\\\"") * "\""
end

escaped_chars = countchars(escape)

println("Part 2")
println(escaped_chars - original_chars)