# Your name: 
# Your student id:
# Your email:
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    d = {}
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT restaurants.name,restaurants.rating,buildings.building,categories.category FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id JOIN categories ON restaurants.category_id = categories.id")
    for restu in cur:
        innder_d = {}
        innder_d["category"] = restu[3]
        innder_d["building"] = restu[2]
        innder_d["rating"] = restu[1]
        d[restu[0]] = innder_d
    cur.close()
    return d

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    d = {}
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    # DATA
    cur.execute("SELECT * FROM categories")
    cats = cur.fetchall()
    for cat in cats:
        cur.execute("SELECT COUNT(restaurants.id) FROM restaurants WHERE restaurants.category_id = ?",(cat[0],))
        d[cat[1]] = int(cur.fetchone()[0])
    # GRAPH is wrong
    lst = sorted(d.items(),key=lambda a:a[1])
    print(lst)
    nums = []
    keys = []
    for item in lst:
        keys.append(item[0])
        nums.append(item[1])
    plt.subplot(1,1,1)
    plt.barh(keys,nums,)
    plt.xlabel("Number of resturaunts")
    plt.ylabel("Category")
    plt.title("Resturaunts per Category in Ann Arbor")
    plt.tight_layout()
    plt.savefig('RestCats.png')
    cur.close()
    return d

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    lst = []
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT id FROM buildings WHERE buildings.building = ?",(building_num,))
    b_id = cur.fetchone()
    cur.execute("SELECT name,rating FROM restaurants WHERE restaurants.building_id = ?",(b_id[0],))
    restus = cur.fetchall()
    restus.sort(key=lambda a:a[1],reverse=True)
    for item in restus:
        lst.append(item[0])
    cur.close()
    return lst

    

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
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
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    # def test_get_highest_rating(self):
    #     highest_rating = get_highest_rating('South_U_Restaurants.db')
    #     self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
