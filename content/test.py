from typing import List


class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        flag_word_started = False
        count = 0
        n = len(s) - 1

        for i in range(0, len(s)):
            if s[n - i] == ' ' and not flag_word_started:
                continue
            elif flag_word_started and s[n - i] == ' ':
                return count
            else:
                flag_word_started = True
                count += 1

        return count

if __name__ == '__main__':
    nums1 = [0, 1, 2, 2, 3, 0, 4, 2]
    nums2 = 2

    solution = Solution()
    print(solution.lengthOfLastWord("d"))
    print(nums1)
# [0,1,4,0,3]