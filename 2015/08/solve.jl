debug = false
filename = if debug "test.txt" else "input.txt" end

lines = readlines(filename)

countchars(func) = sum(length(func(line)) for line in lines)

# Part 1

# there is a built-in function called `unescape_string`
# but it doesn't do the right thing
parse_eval(line) = eval(Meta.parse(line))

original_chars = countchars(identity)
memory_chars = countchars(parse_eval)

println("Part 1")
println(original_chars - memory_chars)

# Part 2

# similarly there is a function called `escape_string` that doesn't do this exactly
escape(line) = "\"" * replace(line, "\\" => "\\\\", "\"" => "\\\"") * "\""

escaped_chars = countchars(escape)

println("Part 2")
println(escaped_chars - original_chars)