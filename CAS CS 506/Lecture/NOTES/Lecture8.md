# 10/7/2024
## Latent Semantic Analysis 
- another applicattion for SVD
- in a matrix, hold a count of words that appears in different papers
- what concepts best represent these documents? Can we write each document as a vector in a space of concepts? 
  - doc-to-term similarity X term-to-concept similary = doc-to-concept similarity 
- Inputs are documents, each word is a feature, we can represent each doc as: 
  - Represent paper as presence of a word (0/1)
    - may have to do some preprocessing -- stemming, filler, etc
- term-to-concept similarity 
  - in theory, there is biology concept on y-axis, computer science on x-axis --> each term is a vector between biology and cs 
  - worsd with similar semantic meanings should be close together 
- another option for representing document: Count of word (0, 1, 2, ...)
  - when multipky by term-to-concept matrix, get higher similarity
- doc-to-concept similarity matrix X "strength" of each concept X term-to-concept similarity matrix 
- one more way of representing docuemnts: most popular!!
  - TfiDf --> tf*idf
  - tf = term frequency in the document 
  - idf = log(number of documents/number of documents that contain the term)
  - if word is very present, then we wan tot penalize by its freqeuncy across other documents..?
    - eg. "the" would be super frequent, bit not important, so penalize so it won't be repressented 