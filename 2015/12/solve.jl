using JSON

debug = false
filename = if debug "test.txt" else "input.txt" end

document = JSON.parsefile(filename)

intsum(x, ignorered::Bool) = 0
intsum(x::Int, ignorered::Bool) = x
intsum(x::AbstractArray, ignorered::Bool) = sum(intsum(v, ignorered) for v in x)
function intsum(x::AbstractDict, ignorered::Bool)
    if ignorered && "red" in values(x) 
        0 
    else
        sum(intsum(v, ignorered) for v in values(x)) 
    end
end

println("Part 1")
println(intsum(document, false))

println("Part 2")
println(intsum(document, true))