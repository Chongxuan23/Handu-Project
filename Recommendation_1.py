# Author: Chongxuan Bi
# Date: 07/08/2020
# Advertises purchases of other people who buy the same product as the person of interest
# Aimed for this particular customer

from collections import *


# Create a function that searches for unique values within the list
def unique(target_list):
    unique_list = []
    for element in target_list:
        if element not in unique_list:
            unique_list.append(element)
    return unique_list


# Create a function that searches for elements in the list other than the reference value
def others(target_list, reference):
    other_elements = []
    for component in target_list:
        if component != reference:
            other_elements.append(component)
    return other_elements


# Read-in file
read_file_name = "orderdata.csv"
with open(read_file_name) as file:
    lines = file.readlines()

# Create a list that consists of every item purchased and its consumer
total_purchases = []
for line in lines[1:]:
    total_purchases.append(line.rstrip().split(sep=","))

# Create a list that consists of all user ids that appear in the data
total_user_ids = []
for purchase in total_purchases:
    total_user_ids.append(purchase[1])

unique_user_ids = unique(total_user_ids)

# Create a list that consists of all SKU's that appear in the data
total_sku = []
for purchase in total_purchases:
    total_sku.append(purchase[2])

# Create a list that consists of lists, where each list contains a consumer and their purchases
unique_users_purchases = []
for user in unique_user_ids:
    user_purchases = []
    for purchase in total_purchases:
        if purchase[1] == user:
            user_purchases.append(purchase[2])
    if len(user_purchases) > 1:     # Only include customers with multiple purchases
        user_purchases.insert(0, user)
        unique_users_purchases.append(user_purchases)

# Find frequencies of items purchased
sku_freq = Counter(total_sku)
frequencies = sku_freq.most_common()

# Create a list that contains items that are purchased more than one time
multiple_purchase_items = []
for frequency in frequencies:
    if frequency[1] >= 2:
        multiple_purchase_items.append(frequency[0])

# Create a list that contains lists, where each list consists of an item followed by user ids that purchased this item
all_customers_same_purchase = []
for multiple_purchase_item in multiple_purchase_items:
    customers_same_purchase = []
    for purchase in total_purchases:
        if purchase[2] == multiple_purchase_item:
            customers_same_purchase.append(purchase[1])
    customers_same_purchase.insert(0, multiple_purchase_item)
    all_customers_same_purchase.append(customers_same_purchase)

# Create a list that contains lists, where each list consists of a user id followed by recommended items.
# Note that duplicate user ids appear, and that under a single user_id, duplicate recommendations appear.
duplicate_recommendations_duplicate_users = []
for customers_same_purchase in all_customers_same_purchase:
    for customer in customers_same_purchase[1:]:
        each_customer_recommendations = []
        other_customers = others(customers_same_purchase[1:], customer)
        for user_purchases in unique_users_purchases:
            if user_purchases[0] in other_customers:
                each_customer_recommendations.extend(user_purchases[1:])
        each_customer_recommendations.insert(0, customer)
        duplicate_recommendations_duplicate_users.append(each_customer_recommendations)

# Create a list that contains all recommended (maybe duplicate) users.
duplicate_users = []
for recommendations_duplicate_user in duplicate_recommendations_duplicate_users:
    duplicate_users.append(recommendations_duplicate_user[0])

unique_users = unique(duplicate_users)

# Remove duplicate appearances of user ids in recommendations.
duplicate_recommendations_unique_users = []
for unique_user in unique_users:
    unique_user_recommendations = []
    for duplicate_recommendations_duplicate_user in duplicate_recommendations_duplicate_users:
        if duplicate_recommendations_duplicate_user[0] == unique_user:
            unique_user_recommendations.extend(duplicate_recommendations_duplicate_user[1:])
    unique_user_recommendations.insert(0, unique_user)
    duplicate_recommendations_unique_users.append(unique_user_recommendations)

# Sort recommendations for each user by their number of appearances
unique_recommendations_unique_users = []
for duplicate_recommendations_unique_user in duplicate_recommendations_unique_users:
    recommendations_freq = Counter(duplicate_recommendations_unique_user[1:])
    sorted_recommendations_freq = recommendations_freq.most_common()

    unique_sorted_recommendations = []
    for sorted_recommendation_freq in sorted_recommendations_freq:
        unique_sorted_recommendations.append(sorted_recommendation_freq[0])

    unique_sorted_recommendations.insert(0, duplicate_recommendations_unique_user[0])
    unique_recommendations_unique_users.append(unique_sorted_recommendations)


print(unique_recommendations_unique_users)
"""
# Output the recommendations
output_file_name = "Recommendation_1.csv"
with open(output_file_name, "w") as file:
    for unique_recommendations_unique_user in unique_recommendations_unique_users:
        string = ", ".join(unique_recommendations_unique_user)
        file.write(string + "\n")
"""