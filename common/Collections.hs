module Collections
  ( pairwise,
    pairwiseDifference,
    allPairwise,
  )
where

pairwise f xs = zipWith f xs (tail xs)

pairwiseDifference :: (Num a) => [a] -> [a]
pairwiseDifference = pairwise (-)

allPairwise f xs = all (uncurry f) (zip xs (tail xs))
