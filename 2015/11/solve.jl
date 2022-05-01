using IterTools

debug = false
filename = if debug "test.txt" else "input.txt" end

line = readline(filename)

badletters = Set(('i', 'o', 'l'))

function increment(string)
    position = length(string)
    carry = 1

    vec = [c for c in string]

    while carry > 0
        if vec[position] == 'z'
            vec[position] = 'a'
            carry = 1
            position -= 1
            if position <= 0
                position = length(vec)
                carry = 0
            end
        else
            vec[position] += 1
            carry = 0
            if vec[position] in badletters
                carry = 1
            end
        end
    end

    return join(vec, "")
end

@assert increment("az") == "ba"
@assert increment("zz") == "aa"


function has_straight(string)
    vec = [c for c in string]
    for group in groupby(identity, diff(vec))
        if group[1] == 1 && length(group) >= 2
            return true
        end
    end

    return false
end

@assert has_straight("abc")

function has_pairs(string)
    pair_chars = Set()
    for group in groupby(identity, string)
        if length(group) >= 2
            push!(pair_chars, group[1])
        end
    end

    return length(pair_chars) >= 2
end

@assert has_pairs("aabb")
@assert !has_pairs("abcdd")
@assert !has_pairs("aabaa")


function valid(password)
    return (
        has_straight(password)
        && isdisjoint(badletters, password)
        && has_pairs(password)
    )
end

@assert !valid("hijklmmn")
@assert !valid("abbceffg")
@assert !valid("abbcegjk")

function nextpassword(password)
    # fast forward to next after bad letters
    for i in 1:length(password)
        if password[i] in badletters
            password = join([
                password[1:i]; 
                repeat("z", length(password)-i)])
            break
        end
    end

    while true
        password = increment(password)
        if valid(password)
            break
        end
    end

    return password
end

@assert nextpassword("abcdefgh") == "abcdffaa"
@assert nextpassword("ghijklmn") == "ghjaabcc"

println("Part 1")
p = nextpassword(line)
println(p)

println("Part 2")
println(nextpassword(p))