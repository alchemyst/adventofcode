using StatsBase

lines = map(collect, readlines("sample.txt"))
data = permutedims(hcat(lines...))

function bitcount(bits)
    count = Dict('0' => 0, '1' => 0)
    for i in 1:length(bits)
        count[bits[i]] += 1
    end

    if count['1'] > count['0']
        return '1', '0', false
    elseif count['0'] > count['1']
        return '0', '1', false
    else
        return '0', '1', true
    end
end

bitlength = length(data[1])

gamma_bits = repeat(['0'], bitlength)
epsilon_bits = repeat(['0'], bitlength)

for position in 1:bitlength
    most_common, least_common, tie = bitcount(data[:, position])
    gamma_bits[position] = most_common
    epsilon_bits[position] = least_common
end

toint(s) = parse(Int64, join(s), base=2)

gamma = toint(gamma_bits)
epsilon = toint(epsilon_bits)

print("Part 1")
print(gamma*epsilon)

function apply_bit_criteria(data, hi, position)
    most_common_bit, least_common_bit, same = bitcount(data[:, position])

    if hi
        bitvalue = if same 
            '1' 
        else 
            most_common_bit 
        end
    else
        bitvalue = if same
        '0' else 
            least_common_bit
        end
    end

    newdata = data[data[:, 1] .== '1', :]

    return bitvalue, newdata
end

function bitcheck(data, hi)
    runningdata = copy(data)

    for position in  1:bitlength
        bitvalue, runningdata = apply_bit_criteria(runningdata, hi, position)

        if size(runningdata, 1) == 1
            break
        end
    end

    return join(runningdata[1, :])
end

oxygen_generator_rating = toint(bitcheck(data, true))
CO2_scrubber_rating = toint(bitcheck(data, false))

print("Part 2")
print(oxygen_generator_rating*CO2_scrubber_rating)