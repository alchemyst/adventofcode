debug = false
filename = if debug "test.txt" else "input.txt" end

lines = open(filename) do f
    read(f, String) |> split
end

pairwise(s) = zip(s[1:end-1],  s[2:end])

function nice1(s)
    """
    A nice string is one with all of the following properties:

    It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
    It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
    It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.

    :param s:
    :return:
    """
    vowels = "aeiou"
    bad_strings = ["ab", "cd", "pq", "xy"]

    nvowels = sum(count(v, s) for v in vowels)
    if nvowels < 3
        return false
    end

    doubles = false
    for pair in pairwise(s)
        if pair[1] == pair[2]
            doubles = true
            break
        end
    end

    if !doubles
        return false
    end

    if any(x -> occursin(x, s), bad_strings)
        return false
    end

    return true
end

# Part 1
nice_strings1 = count(nice1, lines)
println("Part 1")
println(nice_strings1)

# Part 2
repeated = r"(..).*\1"
repeated_with_one = r"(.).\1"
nice2(s) = occursin(repeated, s) & occursin(repeated_with_one, s)
nice_strings2 = count(nice2, lines)
println("Part 2")
println(nice_strings2)