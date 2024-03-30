from pymongo import MongoClient

# MongoDB connection (replace with your details)
uri = "..."
client = MongoClient(uri)
db = client['voice_profiles']
collection = db['details']

def get_user_details():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    mobile_number = input("Enter your mobile number: ")
    age = int(input("Enter your age: "))  # Convert age to integer
    return {"name": name, "email": email, "mobile_number": mobile_number, "age": age}

def insert_user_details(details):
    collection.insert_one(details)
    print("User details inserted successfully!")

def get_email_by_name(name):
    user = collection.find_one({"name": {"$regex": f"{name}", "$options": "i"}})
    if user:
        return user["email"]
    else:
        return "User not found"

def get_user_details_by_name(name, field):
    first_name = name.split()[0]
    user = collection.find_one({"name": {"$regex": f"{first_name}", "$options": "i"}}, {field: 1, "_id": 0})
    if user and field in user:
        return user[field]
    else:
        return None

def query_info():
    user_queries = input("Enter your queries in the format 'field of user': ").split(",")
    for user_query in user_queries:
        user_query = user_query.strip().split(" of ")
        if len(user_query) == 2:
            field, name = user_query[0], user_query[1]
            field_value = get_user_details_by_name(name, field)
            if field_value is not None:
                print(f"{field.capitalize()} of {name}: {field_value}")
            else:
                print(f"Field '{field}' not found for {name}")
        else:
            print("Invalid query format. Please use 'field of user'.")

if __name__ == "__main__":
    # Continuous loop for getting user details
    while True:
        user_input = input("Enter 'done' if finished entering user details, or enter to continue: ")
        if user_input.lower() == "done":
            break
        user_details = get_user_details()
        insert_user_details(user_details)

    # Query for information
    while True:
        query_info()
        continue_query = input("Do you want to continue querying? (yes/no): ")
        if continue_query.lower() != "yes":
            print("Okay, exiting...")
            break
