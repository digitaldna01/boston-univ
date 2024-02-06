## Import Julia Package
using Random
using Plots
using StatsBase
using DataFrames
using Statistics
using Distributions

# Toss a fair coin 1000 times and estimate the probability of observing heads using the fraction #heads/#tosses
coin_sides = ["Tails","Heads"]
n_tosses = 1000

random_tosses = rand(coin_sides, n_tosses)

probability_heads = count(==("Heads"), random_tosses) / n_tosses
probability_tails = count(==("Tails"), random_tosses) / n_tosses

println("Probability of Heads: ", probability_heads)
println("Probability of Tails: ", probability_tails)

# Empirical probability of observing Heads vs the number of tosses
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

# Simulation of die rolls and create a bar chart to display the observed frequencies for each face of the die
die = 1:6
n_tosses = 10000
random_tosses = rand(die, n_tosses) ## random_tosses is the array itself
print(random_tosses)
prob = Dict{Int64, Float64}()

for side in die
    prob[side] = count(==(side), random_tosses) / n_tosses
end

println(prob) 

# Represent in Histogram
keys_list = collect(keys(prob))
values_list = collect(values(prob))

println(maximum(values_list)/minimum(values_list))

bar(keys_list, values_list, xlabel="sides", ylabel="probability", title="Empirical probability", ylims=(0,0.2))
hline!([1/6], line=:dash, color=:black)

# For increment try of die toes(10, 20, 30, ..., 100, 200, 300, ... 1000) plot the ration of max and min proabability of sides
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

### BERNOULLI DISTRIBUTION
# Create Bernoulli funtion with P = 0.5
Base.@kwdef struct Bernoulli 
    p::Float64 = 0.5
end    

# trial is the input variable name
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

### BINOMIAL DISTRIBUTION
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

### DISCRETE UNIFORM DISTRIBUTION
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

### MULTIMONIAL DISTRIBUTION
struct MultinomialRV
    outcomes_probs::Dict{Any, Float64} #Any is any type variable
    n::Int   
end

function simulate(multinomial_rv::MultinomialRV)
    outcomes = collect(keys(multinomial_rv.outcomes_probs))
    probabilities = collect(values(multinomial_rv.outcomes_probs))
    multinomial_dist = Multinomial(multinomial_rv.n, probabilities) # ? Iteration Need to define Multinomial
    sample = rand(multinomial_dist)
    return Dict(zip(outcomes, sample))
end

function generate_samples(multinomial_rv::MultinomialRV, num_samples::Int)
    return [simulate(multinomial_rv) for _ in 1:num_samples]
end

outcomes_probs = Dict("A" => 0.2, "B" => 0.3, "C" => 0.5) # Add all the probabilities is 1
multinomial_rv = MultinomialRV(outcomes_probs, 100)  # 10 trials
samples = generate_samples(multinomial_rv, 1000)

### Poisson Distribution
Base.@kwdef struct PoissonRV
    λ::Float64  # Rate parameter (lambda)
end
 

# Simulate function for a Poisson random variable
function simulate(poisson_rv::PoissonRV)
    poisson_dist = Poisson(poisson_rv.λ)
    return rand(poisson_dist)
end
    
# Generate Poisson samples
function generate_samples(poisson_rv::PoissonRV, num_samples::Int)
    return [simulate(poisson_rv) for _ in 1:num_samples]
end

# Example usage: generate 1000 samples from a Poisson distribution with λ=4.0
poisson_rv = PoissonRV(λ=4.0)
samples = generate_samples(poisson_rv, 1000)

# Plot the histogram
histogram(samples, bins=0:maximum(samples)+1, legend=false,
          xlabel="Number of Events", ylabel="Frequency",
          title="Histogram of Poisson Distribution")

### Geometric Random variable
@kwdef struct GeometricRV
    p::Float64=0.5
end

function simulate(geom_rv::GeometricRV)
    return rand(Geometric(geom_rv.p)) # Geometric is a Distributions package
end

function generate_samples(geom_rv::GeometricRV, num_samples::Int)
    return [simulate(geom_rv) for _ in 1:num_samples]
end

# Example usage: generate 1000 samples from a Geometric distribution with p=0.05
geom_rv = GeometricRV(p=0.05)
samples = generate_samples(geom_rv, 1000)

# Plot the histogram
histogram(samples, bins=0:maximum(samples), legend=false,
          xlabel="Number of Trials", ylabel="Frequency",
          title="Histogram of Geometric Distribution")

# Plot a vertical line at the expected value 1/p
vline!([1/geom_rv.p], label="Expected value", color=:red)

### NEGATIVE BINOMIAL RANDOM VARIABLE
@kwdef struct NegativeBinomialRV
    r::Int=1        # Number of failures until stopping, by default we set it a Geom(p)
    p::Float64=0.1  # Probability of success
end


# Simulate function for a Negative Binomial random variable
function simulate(negbin_rv::NegativeBinomialRV)
    return rand(NegativeBinomial(negbin_rv.r, negbin_rv.p))
end

# Generate negative binomial samples
function generate_samples(negbin_rv::NegativeBinomialRV, num_samples::Int)
    return [simulate(negbin_rv) for _ in 1:num_samples]
end

# Example usage: generate 1000 samples from a Negative Binomial distribution with r=3, p=0.5
negbin_rv = NegativeBinomialRV(r=3, p=0.1)
samples = generate_samples(negbin_rv, 10000)

# Calculate the empirical mean of the samples
empirical_mean = mean(samples)

# Plot the histogram
histogram(samples, bins=0:maximum(samples)+1, legend=false,
          xlabel="Number of Successes", ylabel="Frequency",
          title="Histogram of Negative Binomial Distribution")

# Plot a vertical line at the expected value r/p
vline!([negbin_rv.r/negbin_rv.p], label="Mean value", color=:red)
vline!([mean(samples)], label="Expected value", color=:black)

### Gaussian Distribution
@kwdef struct GaussianRV
    μ::Float64=0  # Mean
    σ²::Float64=1  # Variance
end

function simulate(gaussian_rv::GaussianRV)
    σ = sqrt(gaussian_rv.σ²)  # Standard deviation is the square root of the variance
    return rand(Normal(gaussian_rv.μ, σ)) # package function
end

function generate_samples(gaussian_rv::GaussianRV, num_samples::Int)
    return [simulate(gaussian_rv) for _ in 1:num_samples]
end

gaussian_rv = GaussianRV(μ=0, σ²=10)
samples = generate_samples(gaussian_rv, 10000)

empirical_mean = mean(samples)

# Plot the histogram
histogram(samples, bins=50, legend=false,
          xlabel="Value", ylabel="Frequency",
          title="Histogram of Gaussian Distribution")

# Plot a vertical line at the mean μ
vline!([gaussian_rv.μ], label="Mean", color=:red)


### LAPLACE DISTRIBUTION
@kwdef struct LaplaceRV
    μ::Float64=0  # Mean
    b::Float64=1  # scale parameter
end
 
function simulate(laplace_rv::LaplaceRV)
    return rand(Laplace(laplace_rv.μ, laplace_rv.b))
end

function generate_samples(laplace_rv::LaplaceRV, num_samples::Int)
    return [simulate(laplace_rv) for _ in 1:num_samples]
end

laplace_rv = LaplaceRV(μ=0, b=1)
samples = generate_samples(laplace_rv, 10000)


histogram(samples, bins=50, legend=false,
          xlabel="Value", ylabel="Frequency",
          title="Histogram of Laplace Distribution")

vline!([laplace_rv.μ], label="Mean", color=:red)


### BETA DISTRIBUTION
using Distributions
using Plots

# Number of samples to draw
num_samples = 10000

# Define parameters for the beta distributions
params = [(1, 1), (2, 5), (5,2), (2, 20)]

# Create beta distribution objects with the specified parameters
distributions = [Beta(a, b) for (a, b) in params]

# Generate samples and plot histograms for each set of parameters
histograms = []
for dist in distributions
    samples = rand(dist, num_samples)
    push!(histograms, histogram(samples, bins=50, alpha=0.6, label="a=
(dist.β)"))
end

# Combine the histograms into a single plot
plot(histograms..., layout=(2,2), legend=:topright, xlabel="Value", ylabel="Frequency") 

### COMPARE GAUSSIAN and LAPLACE DISTRIBUTION
function draw_distributions(x)
    normal_dist = pdf.(Normal(0, 1), x)
    uniform_dist = pdf.(Uniform(-1, 1), x)
    laplace_dist = pdf.(Laplace(0, 1), x)

    plot(x, normal_dist, color="blue", linestyle=:solid, label="Gaussian")
    plot!(x, uniform_dist, color="green", linestyle=:dash, label="Uniform")
    plot!(x, laplace_dist, color="red", linestyle=:dot, label="Laplace")

    ylims!(0, 0.61)
    xlabel!("x")
    ylabel!("$p(x)") 
end

x = -4:0.01:4
draw_distributions(x)

### Algorithm for Estimating π using 2d uniform random variables
function approximate_pi(n_exp=100)
    df = DataFrame(x=[], y=[], inside=[]) # Use DataFrame to make array of x, y coordinate and distance from the center point to acknowledge inside the circle
    for i in 1:n_exp
        x, y = rand(), rand()
        push!(df, (x, y, (x-0.5)^2 + (y-0.5)^2 <= 0.5^2)) # for 3rd attribute push
    end
    pi_estimate = 4 * mean(df[!, :inside])
    println("π estimate ", pi_estimate)
    return pi_estimate, df
end

n_exp = 2000
pi_estimate, df = approximate_pi(n_exp)

colors = [flag ? :red : :blue for flag in df[!, :inside]]

scatter(df[!, :x], df[!, :y], color=colors, xlims=(-0.01, 1.01), ylims=(-0.01, 1.01), label="Points", title="Estimating π", aspect_ratio=:equal)
plot!(0:0.01:1, x -> sqrt(0.5^2 - (x - 0.5)^2) + 0.5, color=:black, label="circle")
plot!(0:0.01:1, x -> -sqrt(0.5^2 - (x - 0.5)^2) + 0.5, color=:black, label="")

### Monty Hall Problem
N = 10000 # we repeat the simulation N times
M = 10 # and we will show what happened the first M times 

doors = [1, 2, 3]

door_with_car = rand(doors, N)
println("Placing the car behind one door:\t", join(door_with_car[1:M], " ")) # Show first M places of Car

# player makes a first guess about the door that contains the car
first_guess = rand(doors, N)
println("Player chooses one door:\t\t", join(first_guess[1:M], " "))

# Function to select a door different from the chosen ones
function select_other(chosen, doors)
    return setdiff(doors, chosen)[1]
end

 
revealed_door = [select_other([first_guess[i], door_with_car[i]], doors) for i in 1:N]
println("Host opens other door with no car:\t", join(revealed_door[1:M], " "))

second_guess_A = first_guess
println("\nStrategy A, player keeps first guess:\t", join(second_guess_A[1:M], " "))
success_A = (second_guess_A .== door_with_car)
println("Result:\t\t\t\t\t", join((x -> x ? 'W' : 'L').(success_A[1:M]), " "))

# Strategy B: player switches to the remaining door
second_guess_B = [select_other([first_guess[i], revealed_door[i]], doors) for i in 1:N]
println("\nStrategy B, player switches:\t\t", join(second_guess_B[1:M], " "))
success_B = (second_guess_B .== door_with_car)
println("Result:\t\t\t\t\t", join((x -> x ? 'W' : 'L').(success_B[1:M]), " "))

# calculate the success rate for each strategy
success_rate_A = sum(success_A) / N
success_rate_B = sum(success_B) / N

println("\nSuccess rate of Non-Switch Strategy A: ", success_rate_A)
println("Success rate of Switch Strategy B: ", success_rate_B)

### Online Hiring Problem
function online_maximum(scores, k)
    n = length(scores) # number of candidates
    bestscore = maximum(scores[1:k]) # best score among the first k candidates
    
    best_position = k  
    for i = k+1:n
        if scores[i] > bestscore || i==n
            bestscore = scores[i]
            best_position = i
            break 
        end
    end
    
    return bestscore == maximum(scores)

end

# Example Score
scores = [1,2,10,4,7,6,8]     
# for which k will we get true? 

using Base.MathConstants: e

f(x, n) = (x / n) * log(n / x)

# Set the value of n
n = 100

x_values = 1:1:n

y_values = f.(x_values, n)

plot(x_values, y_values, label="f(x) = x/n * ln(n/x)", xlabel="x", ylabel="f(x)")

vline!([n/e], label="x = n/e", color=:red)