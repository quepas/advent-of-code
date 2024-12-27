import Collections (allPairwise, pairwise, pairwiseDifference)

parseLevels :: String -> [Int]
parseLevels row = map read (words row)

parseFile :: String -> [[Int]]
parseFile content = map parseLevels (lines content)

allIncreasing :: [Int] -> Bool
allIncreasing = all (\x -> x > 0 && x <= 3)

allDecreasing :: [Int] -> Bool
allDecreasing = all (\x -> x >= -3 && x < 0)

isSafeReport :: [Int] -> Bool
isSafeReport values = do
  let level_diff = pairwiseDifference values
  allIncreasing level_diff || allDecreasing level_diff

main :: IO ()
main = do
  content <- readFile "2024/02/input"
  let reports = parseFile content
  let num_safe_reports = sum $ map (fromEnum . isSafeReport) reports
  print num_safe_reports
