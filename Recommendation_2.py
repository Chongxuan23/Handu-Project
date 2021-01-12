# Author: Chongxuan Bi
# Date: 07/06/2020
# Recommendations Among Products Algorithm
# Aimed for this particular product

from collections import *

# Import data
with open("orderdata.csv") as file:
    lines = file.readlines()

# Obtain all order ids
order_id = []

for line in lines:
    order_id.append(line.split(sep=",")[0])

# Define a function that finds unique elements in a list
def unique(target_list):
    unique_list = []
    for element in target_list:
        if element not in unique_list:
            unique_list.append(element)
    return unique_list

# Obtain unique order ids
unique_ids = unique(order_id)

# Obtain purchases for each customer
purchases_all = []

for unique_id in unique_ids:
    purchases_one = []
    for line in lines:
        if line.split(sep=",")[0] == unique_id:
            purchases_one.append(line.split(sep=",")[2].rstrip())
    if len(purchases_one) > 1:
        purchases_all.append(purchases_one)
    else:
        purchases_all = purchases_all

# Define a function that selects every element except the reference
def others(target_list, reference):
    other_elements = []
    for component in target_list:
        if component != reference:
            other_elements.append(component)
    return other_elements


# Obtain bought together items for each reference
# Note that duplicate references & duplicate recommended items appear
total_recommendations = []

for purchases_single in purchases_all:
    for purchase in purchases_single:
        single_recommendations = others(purchases_single, purchase)
        single_recommendations.insert(0, purchase)
        total_recommendations.append(single_recommendations)

# Obtain unique references
unique_references = []

for single_recommendations in total_recommendations:
    reference = single_recommendations[0]
    if reference not in unique_references:
        unique_references.append(reference)


# Obtain recommendations for unique references
# Note that duplicate recommendations appear
unique_references_recommendations = []

for unique_reference in unique_references:
    recommendations = []

    for single_recommendations in total_recommendations:
        reference = single_recommendations[0]
        if reference == unique_reference:
            recommendations.extend(single_recommendations[1:])

    recommendations.insert(0, unique_reference)
    unique_references_recommendations.append(recommendations)

# Obtain unique recommendations for unique references
# The order of recommended items is determined by their frequencies of appearences together with a certain reference
final_recommendations = []

for unique_reference_recommendations in unique_references_recommendations:
    reference = unique_reference_recommendations[0]
    recommendations = unique_reference_recommendations[1:]
    recommendations_freq = Counter(recommendations)
    sorted_recommendations_freq = recommendations_freq.most_common()
    unique_sorted_recommendations = []

    for element in sorted_recommendations_freq:
        unique_sorted_recommendations.append(element[0])

    unique_sorted_recommendations.insert(0, reference)
    final_recommendations.append(unique_sorted_recommendations)

print(final_recommendations)
# Output the recommendations
# file_name = "Recommendation_2.csv"
# with open(file_name, "w") as file:
#     for i in final_recommendations:
#         string = ", ".join(i)
#         file.write(string + "\n")
