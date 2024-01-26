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

plot(coin_tosses, p, legend=false, xlims=(1, 10200), ylims=(0, 1), yticks=0:0:1:1, line=:line, marker=:circle)
hline!([0.5], line=:dash, color=:black)
xlabel!("#Coin tosses")
ylabel!("\$ p_{HEAD} \$")
