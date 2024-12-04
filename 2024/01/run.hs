import Data.List (sort)
import Data.Maybe (fromMaybe)
import qualified Data.Map as Map

-- | Convient alias for a read function
stringToInt :: String -> Int
stringToInt = read

-- | Retrieve N-th column of integers from rows of numbers
getNthColumn :: [String] -> Int -> [Int]
getNthColumn rows column_idx = do
  -- Split numbers by whitespaces
  -- (don't convert yet String to Int, we will do that later with less elements)
  let number_rows = map words rows
  -- Select numbers only from a given column
  let column = [row !! column_idx | row <- number_rows]
  -- Convert the column to integers and sort
  -- Sorting is important because at each time we need to take the next smallest value
  sort (map stringToInt column)

-- | Compute sum of absolute distances between two lists of numbers (part 1)
computeDistance :: [Int] -> [Int] -> Int
computeDistance left_column right_column = sum (map abs (zipWith (-) left_column right_column))

-- | Shorthand for our dictionary Map<Int, Int> type
type CountMap = Map.Map Int Int

-- | Create a map of occurences of each number
countNumbers :: [Int] -> CountMap
countNumbers numbers = do
  -- Each number has count of 1
  let counts = [(x, 1) | x <- numbers]
  -- While creating the map we add values with the same key
  Map.fromListWith (+) counts

-- | Compute sum of similarities between two lists of numbers (part 2)
-- | Similarity means: value * #occurences of value
computeSimilarity :: [Int] -> [Int] -> Int
computeSimilarity left right = do
  let count_map = countNumbers right
  -- Compute similarities and sum them!
  sum (map (\x -> x * fromMaybe 0 (Map.lookup x count_map)) left)

main :: IO()
main = do
  content <- readFile "input"
  let file_lines = lines content
  let left_column = getNthColumn file_lines 0
  let right_column = getNthColumn file_lines 1
  let result_part_1 = computeDistance left_column right_column
  print ("Result Part 1: " ++ show result_part_1)
  let result_part_2 = computeSimilarity left_column right_column
  print ("Result Part 2: " ++ show result_part_2)
