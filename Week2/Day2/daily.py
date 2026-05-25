# Instructions: Pagination System

# 📄 What is Pagination?

# In web development, pagination helps break large lists into smaller, manageable chunks (pages), making it easier to navigate content like search results, product listings, or articles.

# Here’s a visual example:

# Page 1      Page 2      Page 3
# [a, b, c]   [d, e, f]   [g, h, i]

# Goal:

# Create a Pagination class that simulates a basic pagination system.

# Step 1: Create the Pagination Class

# Define a class called Pagination to represent paginated content.
# It should optionally accept a list of items and a page size when initialized.

# Step 2: Implement the __init__ Method

# Accept two optional parameters:
# items (default None): a list of items
# page_size (default 10): number of items per page

# Behavior:

# If items is None, initialize it as an empty list.
# Save page_size and set current_idx (current page index) to 0.
# Calculate total number of pages using math.ceil.

# Step 3: Implement the get_visible_items() Method

# This method returns the list of items visible on the current page.
# Use slicing based on the current_idx and page_size.

# Step 4: Implement Navigation Methods

# These methods should help navigate through pages:

# go_to_page(page_num)
# → Goes to the specified page number (1-based indexing).
# → If page_num is out of range, raise a ValueError.

# first_page()
# → Navigates to the first page.

# last_page()
# → Navigates to the last page.

# next_page()
# → Moves one page forward (if not already on the last page).

# previous_page()
# → Moves one page backward (if not already on the first page).

# 📝 Note:

# Pages are indexed internally from 0, but user input is expected to start at 1.
# All navigation methods (except go_to_page) should return self to allow method chaining.

import math
class Pagination:
    def __init__(self, items=None, page_size=10):
        if page_size <= 0:
            raise ValueError("Page size must be greater than 0")
        self.items = [] if items is None else items
        self.page_size = page_size
        self.current_idx = 0
        self.total_num_pages = math.ceil(len(self.items) / page_size)
        
    def get_visible_items(self):
        start = self.current_idx * self.page_size
        end = start + self.page_size
        return self.items[start:end]
    
    def go_to_page(self, page_num):
        if page_num > self.total_num_pages:
            raise ValueError("Page number is out of range!")
        elif page_num == 0:
            raise ValueError("Page number cannot be 0")
        self.current_idx = page_num - 1
        return self
    
    
    def first_page(self):
        self.current_idx = 0
        return self
    
    def last_page(self):
        if self.total_num_pages > 0:
            self.current_idx = self.total_num_pages - 1        
        return self
    
    def next_page(self):
        if self.current_idx < self.total_num_pages - 1:
            self.current_idx += 1
        return self
    
    def previous_page(self):
        if self.current_idx > 0:
            self.current_idx -= 1
        return self
    
    def __str__(self):
        return "\n".join(str(item) for item in self.get_visible_items())    
    
alphabetList = list("abcdefghijklmnopqrstuvwxyz")
p = Pagination(alphabetList, 4)

print(p.get_visible_items())
# ['a', 'b', 'c', 'd']

p.next_page()
print(p.get_visible_items())
# ['e', 'f', 'g', 'h']

p.last_page()
print(p.get_visible_items())
# ['y', 'z']

p.go_to_page(2)
print(p.current_idx + 1)
# Output: ValueError

p.go_to_page(0)
# Raises ValueError
        
        