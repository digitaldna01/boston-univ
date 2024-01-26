## Import Julia Package
using Random
using Plots
using StatsBase
using DataFrames
using Statistics

## Toss a fair coin 1000 times and estimate the probability of observing heads using the fraction #heads/#tosses
coin_sides = ["Tails","Heads"]
n_tosses = 1000

random_tosses = rand(coin_sides, n_tosses)

probability_heads = count(==("Heads"), random_tosses) / n_tosses
probability_tails = count(==("Tails"), random_tosses) / n_tosses

println("Probability of Heads: ", probability_heads)
println("Probability of Tails: ", probability_tails)

## Empirical probability of observing Heads vs the number of tosses
coin_tosses = union([1], (100:100:1000), (2000:1000:100000))

p = Float64[]

for n_tosses in coin_tosses
    random_tosses = rand(coin_sides, n_tosses)
    probability_heads = count(==("Heads"), random_tosses) / n_tosses
    push!(p, probability_heads)
end

selected_xticks = [coin_tosses[1], coin_tosses[5], coin_tosses[10], coin_tosses[15], coin_tosses[end-1], coin_tosses[end]]

plot(coin_tosses, p,  legend=false, xlims=(1, 10200), ylims=(0, 1), yticks=0:0.1:1, line=:line, marker=:circle, markersize=5, linewidth=4) 
hline!([0.5], line=:dash, color=:black)
xlabel!("#Coin tosses")
ylabel!("\$ p_{HEAD} \$")

## Simulation of die rolls and create a bar chart to display the observed frequencies for each face of the die
die = 1:6
n_tosses = 10000
random_tosses = rand(die, n_tosses) ## random_tosses is the array itself
print(random_tosses)
prob = Dict{Int64, Float64}()

for side in die
    prob[side] = count(==(side), random_tosses) / n_tosses
end

println(prob) 

### Represent in Histogram
keys_list = collect(keys(prob))
values_list = collect(values(prob))

println(maximum(values_list)/minimum(values_list))

bar(keys_list, values_list, xlabel="sides", ylabel="probability", title="Empirical probability", ylims=(0,0.2))
hline!([1/6], line=:dash, color=:black)

### For increment try of die toes(10, 20, 30, ..., 100, 200, 300, ... 1000) plot the ration of max and min proabability of sides
die_tosses = union((10:10:100), (200:100:1000)) ### union makes (10, 20, 30, ... 100, 200, 300, ... 1000)

ratios = Float64[]

for n_tosses in die_tosses
    random_tosses = rand(die, n_tosses)
    prob = Dict(side => count(==(side), random_tosses)/n_tosses for side in die)
    print(prob)
    values_list = collect(values(prob))
    push!(ratios, maximum(values_list)/minimum(values_list))
end

plot(die_tosses, ratios,  legend=false, xlims=(1, 1100), ylims=(0, 10), yticks=0:0.5:10, line=:line, marker=:circle, markersize=5, linewidth=4) 
hline!([1], line=:dash, color=:black)
print(ratios)

### Bernoulli Distribution
### Create Bernoulli funtion with P = 0.5
Base.@kwdef struct Bernoulli 
    p::Float64 = 0.5
end    

### trial is the input variable name
function simulate(trial::Bernoulli)
    return rand() < trial.p ? 1 : 0
end


ber = Bernoulli()
### 1 ~ 10
for i in 1:10
    😺 = simulate(ber)
    println("Result of $(i)-th simulation of Bernoulli with p=$(ber.p) is $(😺)")
end

ber_certainty = Bernoulli(1) ### Bernoulli function with P = 1

for i in 1:10
    😺 = simulate(ber_certainty)
    println("Result of $(i)-th simulation of Bernoulli with p=$(ber_certainty.p) is $(😺)")
end

### Binomial Distribution
Base.@kwdef struct BinomialRV
    n::Int=1000
    p::Float64 = 0.5
end

function simulate(binom_rv::BinomialRV)
    successes = sum(rand() < binom_rv.p for _ in 1:binom_rv.n)
    return successes
end

function generate_samples(binom_rv::BinomialRV, num_samples::Int)
    return [simulate(binom_rv) for _ in 1:num_samples]
end

# Example usage: generate 1000 samples from a Binomial distribution with n=100 and p=0.5
binom_rv = BinomialRV(n=100, p=0.5)
samples = generate_samples(binom_rv, 1000)

histogram(samples, bins=0:binom_rv.n, legend=false, xlabel="Number of Successes", ylabel="Frequesncy", title="Histogram of Binomial Distribution")

### Discrete Uniform distribution
Base.@kwdef struct DiscreteUniformRV # Special case of a discrete uar, could be a set rather than a range
    a::Int=0 # Lower bound
    b::Int=1 # Upper bound, for these default values this is a Bernoulli(0.5)
end

function simulate(du_rv::DiscreteUniformRV)
    return rand(du_rv.a:du_rv.b) ### create one random integer between a and b values of DiscreteUniformRV struct
end

# Generate discrete uniform samples
function generate_samples(du_rv::DiscreteUniformRV, num_samples::Int)
    return [simulate(du_rv) for _ in 1:num_samples] ### generate array of number of random values
end

# Example usage: generate 1000 samples from a Discrete Uniform distribution with bounds of a = 1, b = 6
du_rv = DiscreteUniformRV(a=1, b=6)
samples = generate_samples(du_rv, 10000)

# Calculate frequencies for each outcome
frequencies = countmap(samples) ### frequencies is a dictionary of key int a ~ b, and values of frequency

# Plot the bar chart
bar(collect(du_rv.a:du_rv.b), [get(frequencies, x, 0) for x in du_rv.a:du_rv.b], 
    legend=false, xlabel="Value", ylabel="Frequesncy",
    title="Bar Chart of Discrete Uniform Distribution")

