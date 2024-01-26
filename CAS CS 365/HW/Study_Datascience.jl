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

###
die_tosses = union((10:10:100), (200:100:1000))

ratios = Float64[]

for n_tosses in die_tosses
    random_tosses = rand(die, n_tosses)
    prob = Dict(side => count(==(side), random_tosses)/n_tosses for side in die)
    values_list = collect(values(prob))
    push!(ratios, maximum(values_list)/minimum(values_list))
end



plot(die_tosses, ratios,  legend=false, xlims=(1, 1100), ylims=(0, 10), yticks=0:0.5:10, line=:line, marker=:circle, markersize=5, linewidth=4) 
hline!([1], line=:dash, color=:black)