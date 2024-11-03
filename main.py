from typing import List

class Solution: 
    def remove_duplicates(self, nums:List) -> int:
        """
        Removes duplicates from a sorted non-decreasing integer array in-place.

        Args:
            nums: A list of integers sorted in non-decreasing order.

        Returns:
            The number of unique elements in the array.
        """
        i = 0
        for num in nums:
            # If the current element is different from the previous element (or none), it's unique.
            if i == 0 or num != nums[i - 1]:
                nums[i] = num  # Place the unique element at the write index.
                i += 1  # Increment the write index for the next unique element.

    # The number of unique elements is the write index (i).
        return i

    def count_item(self, nums, k) -> int: 
        d = dict() 
        for item in nums: 
           d[item] = d.get(item, 0) + 1

        return d[k]


if __name__ == '__main__':
    nums = [1, 1, 2, 2, 3]
    s = Solution()
    k = s.remove_duplicates(nums)
    print(f"Number of unique elements: {k}")

    # Print the modified array with underscores for unfilled positions
    print(nums[:k] + ["_"] * (len(nums) - k))