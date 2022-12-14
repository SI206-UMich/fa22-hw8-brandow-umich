import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """
    # Expected return value:
    # [{'name': 'M-36 Coffee Roasters Cafe', 'category': 'Cafe', 'building': 1101, 'rating': 3.8}, ...]

    # Establish connection to database
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    # Select name from restaurants table, category from categories table, building from buildings table, and rating from restaurants table
    query = """
    SELECT restaurants.name, categories.category, buildings.building, restaurants.rating
    FROM restaurants
    JOIN categories ON restaurants.category_id = categories.id
    JOIN buildings ON restaurants.building_id = buildings.id
    """
    cur.execute(query)

    # Create list of dictionaries, where each dictionary contains data for one restaurant
    restaurant_data = []
    for row in cur:
        restaurant = {
            'name': row[0],
            'category': row[1],
            'building': row[2],
            'rating': row[3]
        }
        restaurant_data.append(restaurant)

    # Close connection to database
    conn.close()

    return restaurant_data





def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the counts of each category.
    """
    # Expected return value:
    # {'Asian Cuisine ': 2, 'Bar': 4, 'Bubble Tea Shop': 2, 'Cafe': 3, 'Cookie Shop': 1, 'Deli': 1, 'Japanese Restaurant': 1, 'Juice Shop': 1, 'Korean Restaurant': 2, 'Mediterranean Restaurant': 1, 'Mexican Restaurant': 2, 'Pizzeria': 2, 'Sandwich Shop': 2, 'Thai Restaurant': 1}

    # Establish connection to database
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    # Select category from categories table and count number of restaurants in each category
    query = """
    SELECT categories.category, COUNT(*)
    FROM restaurants
    JOIN categories ON restaurants.category_id = categories.id
    GROUP BY categories.category
    """
    cur.execute(query)

    # Create dictionary of restaurant categories and counts
    restaurant_categories = {}
    for row in cur:
        restaurant_categories[row[0]] = row[1]

    # Close connection to database
    conn.close()

    # Create bar chart
    # Sort categories by count in ascending order
    plt.barh(*zip(*sorted(restaurant_categories.items(), key=lambda x: x[1], reverse=False)))
    
    # Set title, x-axis label, and y-axis label
    plt.title('Restaurant Categories')

    # Set x and y axis limits
    plt.xlabel('Count')
    plt.ylabel('Category')

    # Keep it tight
    plt.tight_layout()

    # Save and show bar chart
    plt.savefig(os.path.join(os.path.dirname(__file__), 'restaurant_categories.png'))
    plt.show()
    plt.close()

    return restaurant_categories

#EXTRA CREDIT
def highest_rated_category(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each category and returns a tuple containing the
    category name of the highest rated restaurants and the average rating of the restaurants
    in that category. This function should also create a bar chart that displays the categories along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """
    # Expected return value:
    # ('Deli', 4.6)

    # Establish connection to database
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    # Select category from categories table and average rating of restaurants in each category
    query = """
    SELECT categories.category, AVG(restaurants.rating)
    FROM restaurants
    JOIN categories ON restaurants.category_id = categories.id
    GROUP BY categories.category
    """
    cur.execute(query)

    # Create dictionary of restaurant categories and average ratings
    restaurant_categories = {}
    for row in cur:
        restaurant_categories[row[0]] = row[1]

    # Close connection to database
    conn.close()

    # Create bar chart
    # Sort categories by average rating in descending order
    plt.barh(*zip(*sorted(restaurant_categories.items(), key=lambda x: x[1], reverse=False)))
    
    # Set title, x-axis label, and y-axis label
    plt.title('Highest Rated Categories')

    # Set x and y axis limits
    plt.xlabel('Average Rating')
    plt.ylabel('Category')

    # Keep it tight
    plt.tight_layout()

    # Save and show bar chart
    plt.savefig(os.path.join(os.path.dirname(__file__), 'highest_rated_categories.png'))
    plt.show()
    plt.close()

    # Find category with highest average rating
    best_category = max(restaurant_categories.items(), key=lambda x: x[1])

    return best_category

#Try calling your functions here
def main():
    print('get_restaurant_data')
    get_restaurant_data('South_U_Restaurants.db')
    print('barchart_restaurant_categories')
    barchart_restaurant_categories('South_U_Restaurants.db')
    print('highest_rated_category')
    highest_rated_category('South_U_Restaurants.db')


class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_category = ('Deli', 4.6)

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_highest_rated_category(self):
        best_category = highest_rated_category('South_U_Restaurants.db')
        self.assertIsInstance(best_category, tuple)
        self.assertEqual(best_category, self.best_category)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
