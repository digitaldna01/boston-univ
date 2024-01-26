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
