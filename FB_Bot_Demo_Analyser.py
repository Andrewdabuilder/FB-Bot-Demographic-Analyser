import csv
from selenium import webdriver

# Set up the webdriver
driver = webdriver.Firefox()

# Navigate to the Facebook login page and log in
driver.get("https://www.facebook.com/login")
username_element = driver.find_element_by_id("email")
password_element = driver.find_element_by_id("pass")
username_element.send_keys("andrew@filterhealth.co")
password_element.send_keys("Lovephonetime8*")
password_element.submit()

# Navigate to the search page and search for "COPD groups"
driver.get("https://www.facebook.com/groups/copdinformationandsupport")

# Scroll down to load more groups
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Find all of the group elements
groups = driver.find_elements_by_css_selector("._32mo")

# Create a CSV file to store the results
with open("copd_groups.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "Profile URL", "Age", "Sex", "Location"])

    # Iterate over the groups
    for group in groups:
        # Click on the group to go to its page
        group.click()

        # Find all of the members in the group
        members = driver.find_elements_by_css_selector("._2uju ._60rg")

        # Iterate over the members
        for member in members:
            # Extract the member's name, profile URL, age, sex, and location
            name = member.find_element_by_css_selector("._60ri").text
            profile_url = member.find_element_by_css_selector("._60ri").get_attribute("href")
            try:
                age_sex_location = member.find_element_by_css_selector("._60rj").text
                age = age_sex_location.split(",")[0]
                sex = age_sex_location.split(",")[1]
                location = age_sex_location.split(",")[2]
            except:
                age = "N/A"
                sex = "N/A"
                location = "N/A"
            
            # Write the member's information to the CSV file
            writer.writerow([name, profile_url, age, sex, location])
        
        # Go back to the search results page
        driver.execute_script("window.history.go(-1)")

# Close the webdriver
driver.close()