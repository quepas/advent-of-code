module Collections
  ( pairwise,
    pairwiseDifference,
    allPairwise,
  )
where

pairwise :: (a -> a -> a) -> [a] -> [a]
pairwise f xs = zipWith f xs (tail xs)

pairwiseDifference :: (Num a) => [a] -> [a]
pairwiseDifference = pairwise (-)

allPairwise :: (a -> a -> Bool) -> [a] -> Bool
allPairwise f xs = all (uncurry f) (zip xs (tail xs))
