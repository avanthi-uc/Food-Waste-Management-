import streamlit as st
import mysql.connector
from mysql.connector import Error
import streamlit as st
import pandas as pd
import datetime


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123",
    database="food_management"
)


st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a page:",
    [
        "📘 Project Introduction",
        "📂 View Tables",
        "🔍 Find Info",
        "🛠️ CRUD Operations",
        "📊 SQL Queries and Visualisation",
        "🧠 Learner SQL Queries",
        "👤 User Introduction"
    ]
)


st.markdown(
    """
    <style>
    /* Main page */
    .stApp {
        background-color: white;
        color: black;
    }

    /* Sidebar (navigation) */
    section[data-testid="stSidebar"] {
        background-color: black;
    }

    /* Sidebar text/icons */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)



if page == "📘 Project Introduction":
        st.header("📘 Project Introduction")

        st.write("""
        **Food wastage** is a significant issue, with many households and restaurants discarding surplus food while numerous people struggle with food insecurity.

        This project aims to develop a **Local Food Wastage Management System**, where:

        - Restaurants and individuals can list surplus food.
        - NGOs or individuals in need can claim the food.
    
        """)

        st.write("""
        -PROVIDER:Restaurants,households and businesses list surplus food.
                 
        -RECEIVERS: NGO's and othe individuals who are in need claim the food.
        
                 """)
    

elif page == "📂 View Tables":
        st.header("📊 View Tables")

        table_option = st.selectbox(
            "Select a table to view:",
            ["Receivers", "Providers", "Food listings", "Claims"]
        )

        csv_files = {
            "Receivers": "receivers_data.csv",
            "Providers": "providers_data.csv",
            "Food listings": "food_listings_data.csv",
            "Claims": "claims_data.csv"
        }

        selected_file = csv_files[table_option]

        df = pd.read_csv(selected_file)
        st.dataframe(df)
        

elif page == "🛠️ CRUD Operations":
        st.header("🛠️ CRUD Operations")

        crud_table = st.selectbox(
            "Select a table to perform CRUD operations:",
            ["Receivers", "Claims", "Food Listings", "Providers"]
        )

        st.write(f"You selected the **{crud_table}** table.")

        operation = st.selectbox(
            "Select an operation:",
            ["Add", "Update", "Delete","View"]
        )

        st.write(f"Selected Operation: **{operation}**")

        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root@123",
        database="food_management"
                        )
        cursor = conn.cursor()

        if crud_table == "Receivers":
            if operation == "Add":
        
                st.subheader("Add New Receiver")

                receiver_id = st.number_input("Receiver ID", min_value=1, step=1, format="%d")
                name = st.text_input("Name")
                receiver_type = st.selectbox("Type", ["Shelter", "NGO", "Individual", "Charity"])
                city = st.text_input("City")
                contact = st.text_input("Contact Number")

                if st.button("Add Receiver"):
                    if not all([receiver_id, name, receiver_type, city, contact]):
                        st.warning("Please fill out all fields.")
                    else:
                        try:
                            query = """
                            INSERT INTO Receivers (receiver_id, name, type, city, contact)
                            VALUES (%s, %s, %s, %s, %s)
                            """
                            cursor.execute(query, (int(receiver_id), name, receiver_type, city, contact))
                            conn.commit()
                            st.success("✅ Receiver added successfully!")
                        except Error as e:
                            st.error("❌ Failed to add receiver:")

            elif operation == "Update":
                st.subheader("Update Receiver Record")
                try:
                    cursor.execute("SELECT receiver_id FROM Receivers")
                    receiver_ids = [row[0] for row in cursor.fetchall()]
                except Error as e:
                    st.error(f"Error fetching receiver IDs: {e}")
                    receiver_ids = []

                if receiver_ids:
                    selected_id = st.selectbox("Select Receiver ID to update", receiver_ids)

            
                try:
                    cursor.execute("SELECT name, type, city, contact FROM Receivers WHERE receiver_id = %s", (selected_id,))
                    record = cursor.fetchone()
                except Error as e:
                    st.error(f"Error fetching receiver data: {e}")
                    record = None

                if record:
                    name = st.text_input("Name", value=record[0])
                    receiver_type = st.selectbox("Type", ["Shelter", "NGO", "Individual", "Charity"], index=["Shelter", "NGO", "Individual", "Charity"].index(record[1]))
                    city = st.text_input("City", value=record[2])
                    contact = st.text_input("Contact Number", value=record[3])

                if st.button("Update Receiver"):
                    try:
                        update_query = """
                            UPDATE Receivers
                            SET name = %s, type = %s, city = %s, contact = %s
                            WHERE receiver_id = %s
                        """
                        cursor.execute(update_query, (name, receiver_type, city, contact, selected_id))
                        conn.commit()
                        st.success("Receiver updated successfully!")
                    except Error as e:
                        st.error(f"Failed to update receiver: {e}")
                else:
                    st.warning("No receivers found in the database.")

            elif operation == "Delete":
                st.subheader(" Delete Receiver Record")

                try:
                    cursor.execute("SELECT receiver_id FROM Receivers")
                    receiver_ids = [row[0] for row in cursor.fetchall()]
                except Error as e:
                    st.error(f"Error fetching receiver IDs: {e}")
                    receiver_ids = []

                if receiver_ids:
                    selected_id = st.selectbox("Select Receiver ID to delete", receiver_ids)

                    if st.button("Delete Receiver"):
                        try:
                            cursor.execute("DELETE FROM Receivers WHERE receiver_id = %s", (selected_id,))
                            conn.commit()
                            st.success(f" Receiver ID {selected_id} deleted successfully!")
                        except Error as e:
                            st.error(f" Failed to delete receiver: {e}")
                    else:
                        st.warning("No receiver records found to delete.")

            elif operation == "View":
                st.subheader("View Receiver Details")

                try:
                    cursor.execute("SELECT receiver_id FROM Receivers")
                    receiver_ids = [row[0] for row in cursor.fetchall()]
                except Error as e:
                    st.error(f"Error fetching receiver IDs: {e}")
                    receiver_ids = []

                if receiver_ids:
                    selected_id = st.selectbox("Select Receiver ID to view", receiver_ids)

                    try:
                        cursor.execute("""
                        SELECT receiver_id, name, type, city, contact
                        FROM Receivers WHERE receiver_id = %s
                    """, (selected_id,))
                        record = cursor.fetchone()

                        if record:
                            st.markdown("### Receiver Information")
                            st.write(f"**ID:** {record[0]}")
                            st.write(f"**Name:** {record[1]}")
                            st.write(f"**Type:** {record[2]}")
                            st.write(f"**City:** {record[3]}")
                            st.write(f"**Contact:** {record[4]}")
                        else:
                            st.warning("No data found for this Receiver ID.")
                    except Error as e:
                        st.error(f"Error retrieving receiver details: {e}")
                else:
                    st.warning("No receiver records found.")

        
        elif crud_table == "Providers":
            if operation == "Add":
                st.subheader("Add New Provider")

                provider_id = st.number_input("Provider ID", min_value=1, step=1, format="%d")
                name = st.text_input("Name")
                provider_type = st.selectbox("Type", ["Supermarket", "Grocery Store", "Restaurant", "Catering Service"])
                address = st.text_input("Address")
                city = st.text_input("City")
                contact = st.text_input("Contact Number")

                if st.button("Add Provider"):
                    if not all([provider_id, name, provider_type, address, city, contact]):
                        st.warning("Please fill out all fields.")
                    else:
                         try:
                            cursor.execute("""
                            INSERT INTO Providers (provider_id, name, type, address, city, contact)
                            VALUES (%s, %s, %s, %s, %s, %s)
                         """, (int(provider_id), name, provider_type, address, city, contact))
                            conn.commit()
                            st.success(" Provider added successfully!")
                         except Error as e:
                            st.error(f" Failed to add provider: {e}")


            elif operation == "Update":
                st.subheader("Update Provider Record")

                try:
                    cursor.execute("SELECT provider_id FROM Providers")
                    provider_ids = [row[0] for row in cursor.fetchall()]
                except Error as e:
                    st.error(f"Error fetching provider IDs: {e}")
                    provider_ids = []

                if provider_ids:
                    selected_id = st.selectbox("Select Provider ID to update", provider_ids)

                    try:
                        cursor.execute("SELECT name, type, address, city, contact FROM Providers WHERE provider_id = %s", (selected_id,))
                        record = cursor.fetchone()
                    
                    except Error as e:
                        st.error(f"Error fetching provider data: {e}")
                        record = None
                    if record:
                        name = st.text_input("Name", value=record[0])
                        provider_type = st.selectbox("Type", ["Supermarket", "Grocery Store", "Restaurant", "Catering Service"], index=["Supermarket", "Grocery Store", "Restaurant", "Catering Service"].index(record[1]))
                        address = st.text_input("Address", value=record[2])
                        city = st.text_input("City", value=record[3])
                        contact = st.text_input("Contact Number", value=record[4])
                        if st.button("Update Provider"):
                            try:
                                cursor.execute("""
                                    UPDATE Providers
                                    SET name = %s, type = %s, address = %s, city = %s, contact = %s
                                    WHERE provider_id = %s
                                """, (name, provider_type, address, city, contact, selected_id))
                                conn.commit()
                                st.success(" Provider updated successfully!")      
                            except Error as e:
                               st.error(f" Failed to update provider: {e}")
                else:
                    st.warning("No provider records found.")


            elif operation == "Delete":
                st.subheader("Delete Provider Record")

                try:
                    cursor.execute("SELECT provider_id FROM Providers")
                    provider_ids = [row[0] for row in cursor.fetchall()]
                except Error as e:
                    st.error(f"Error fetching provider IDs: {e}")
                    provider_ids = []

                if provider_ids:
                    selected_id = st.selectbox("Select Provider ID to delete", provider_ids)

                    if st.button("Delete Provider"):
                        try:
                            cursor.execute("DELETE FROM Providers WHERE provider_id = %s", (selected_id,))
                            conn.commit()
                            st.success(f" Provider ID {selected_id} deleted successfully!")
                        except Error as e:
                            st.error(f" Failed to delete provider: {e}")
                else:
                    st.warning("No provider records found to delete.")


            elif operation == "View":
                st.subheader("View Provider Details")

                try:
                    cursor.execute("SELECT provider_id FROM Providers")
                    provider_ids = [row[0] for row in cursor.fetchall()]
                except Error as e:
                    st.error(f"Error fetching provider IDs: {e}")
                    provider_ids = []

                if provider_ids:
                    selected_id = st.selectbox("Select Provider ID to view", provider_ids)

                    try:
                        cursor.execute("""
                            SELECT provider_id, name, type, address, city, contact
                            FROM Providers WHERE provider_id = %s
                        """, (selected_id,))
                        record = cursor.fetchone()

                        if record:
                            st.markdown("### Provider Information")
                            st.write(f"**ID:** {record[0]}")
                            st.write(f"**Name:** {record[1]}")
                            st.write(f"**Type:** {record[2]}")
                            st.write(f"**Address:** {record[3]}")
                            st.write(f"**City:** {record[4]}")
                            st.write(f"**Contact:** {record[5]}")
                        else:
                            st.warning("No data found for this Provider ID.")
                    except Error as e:
                        st.error(f"Error retrieving provider details: {e}")
                else:
                    st.warning("No provider records found.")

        elif crud_table == "Food Listings":
            if operation == "Add":
                st.subheader("Add New Food Listing")

                food_id = st.number_input("Food ID", min_value=1, step=1, format="%d")
                food_name = st.text_input("Food Name")
                quantity = st.number_input("Quantity", min_value=1, step=1)
                expiry_date = st.date_input("Expiry Date")
                provider_id = st.number_input("Provider ID", min_value=1, step=1, format="%d")
                provider_type = st.selectbox("Provider Type", ["Supermarket", "Grocery Store", "Restaurant", "Catering Service"])
                location = st.text_input("Location")
                food_type = st.selectbox("Food Type", ["Vegetarian", "Vegan", "Non-Vegetarian"])
                meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner","Snacks"])

                if st.button("Add Food Listing"):
                    if not all([food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type]):
                        st.warning("Please fill out all fields.")
                    else:
                        try:
                            cursor.execute("SELECT food_id FROM `food_listings` WHERE food_id = %s", (food_id,))
                            if cursor.fetchone():
                                st.error(f"Food ID {food_id} already exists.")
                            else:
                                cursor.execute("SELECT provider_id FROM Providers WHERE provider_id = %s", (provider_id,))
                                if not cursor.fetchone():
                                    st.error(f"Provider ID {provider_id} does not exist.")
                                else:
                                    cursor.execute("""
                                        INSERT INTO `food_listings` 
                                        (food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    """, (food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type))
                                    conn.commit()
                                    st.success(" Food listing added successfully!")
                        except Error as e:
                            st.error(f" Failed to add food listing: {e}")
            
            elif operation == "Update":
                st.subheader("Update Food Listing")

                try:
                    cursor.execute("SELECT food_id FROM food_listings")
                    food_ids = [row[0] for row in cursor.fetchall()]
                except Error as e:
                    st.error(f"Error fetching food IDs: {e}")
                    food_ids = []

                if food_ids:
                    selected_id = st.selectbox("Select Food ID to update", food_ids)

                    try:
                        cursor.execute("""
                            SELECT food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type
                            FROM `food_listings` WHERE food_id = %s
                        """, (selected_id,))
                        record = cursor.fetchone()
                    except Error as e:
                        st.error(f"Error fetching listing: {e}")                            
                        record = None

                    if record:
                        food_name = st.text_input("Food Name", value=record[0])
                        quantity = st.number_input("Quantity", min_value=1, step=1, value=record[1])
                        expiry_date = st.date_input("Expiry Date", value=record[2])
                        provider_id = st.number_input("Provider ID", min_value=1, step=1, format="%d", value=record[3])
                        provider_type = st.selectbox("Provider Type", ["Supermarket", "Grocery Store", "Restaurant", "Catering Service"], index=["Supermarket", "Grocery Store", "Restaurant", "Catering Service"].index(record[4]))
                        location = st.text_input("Location", value=record[5])
                        food_type = st.selectbox("Food Type", ["Vegetarian", "Vegan", "Non-Vegetarian"], index=["Vegetarian", "Vegan", "Non-Vegetarian"].index(record[6]))
                        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner","Snacks"], index=["Breakfast", "Lunch", "Dinner","Snacks"].index(record[7]))

                        if st.button("Update Listing"):
                            try:
                                cursor.execute("SELECT provider_id FROM Providers WHERE provider_id = %s", (provider_id,))
                                if not cursor.fetchone():
                                    st.error(f" Provider ID {provider_id} does not exist.")
                                else:
                                    cursor.execute("""
                                        UPDATE `food_listings`
                                        SET food_name = %s, quantity = %s, expiry_date = %s,
                                            provider_id = %s, provider_type = %s, location = %s,
                                            food_type = %s, meal_type = %s
                                        WHERE food_id = %s
                                    """, (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type, selected_id))
                                    conn.commit()
                                    st.success(" Food listing updated successfully!")
                            except Error as e:
                                st.error(f" Failed to update listing: {e}")

                else:
                     st.warning("No food listings found to update.")


            elif operation == "Delete":
                st.subheader("Delete Food Listings Record")

                try:
                    cursor.execute("SELECT food_id FROM food_listings")
                    food_ids = [row[0] for row in cursor.fetchall()]
                except Error as e:
                    st.error(f"Error fetching provider IDs: {e}")
                    food_ids = []

                if food_ids:
                    selected_id = st.selectbox("Select Food ID to delete", food_ids)

                    if st.button("Delete Food Listing"):
                        try:
                            cursor.execute("DELETE FROM food_listings WHERE food_id = %s", (selected_id,))
                            conn.commit()
                            st.success(f" FOOD ID {selected_id} deleted successfully!")
                        except Error as e:
                            st.error(f" Failed to delete food listing: {e}")
                else:
                    st.warning("No food listing records found to delete.")

            
            elif operation == "View":
                st.subheader("View Food Listing Details")

                try:
                    cursor.execute("SELECT food_id FROM food_listings")
                    food_ids = [row[0] for row in cursor.fetchall()]
                except Error as e:
                    st.error(f"Error fetching food IDs: {e}")
                    food_ids = []

                if food_ids:
                    selected_id = st.selectbox("Select Food ID to view", food_ids)

                    try:
                        cursor.execute("""
                            SELECT food_id, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type
                            FROM food_listings WHERE food_id = %s
                        """, (selected_id,))
                        record = cursor.fetchone()

                        if record:
                            st.markdown("### Food Listing Information")
                            st.write(f"**Food ID:** {record[0]}")
                            st.write(f"**Quantity:** {record[1]}")
                            st.write(f"**Expiry Date:** {record[2]}")
                            st.write(f"**Provider ID:** {record[3]}")
                            st.write(f"**Provider Type:** {record[4]}")
                            st.write(f"**Location:** {record[5]}")
                            st.write(f"**Food Type:** {record[6]}")
                            st.write(f"**Meal Type:** {record[7]}")
                        else:
                            st.warning("No data found for this Food ID.")
                    except Error as e:
                        st.error(f"Error retrieving food listing details: {e}")
                else:
                    st.warning("No food listing records found.")


        
            

        elif crud_table == "Claims":
            if operation == "Update":
                st.subheader("Update Claim")

                cursor.execute("SELECT claim_id FROM claims")
                claim_ids = [row[0] for row in cursor.fetchall()]

                if claim_ids:
                    selected_claim = st.selectbox("Select Claim ID to update", claim_ids)

                    cursor.execute("SELECT food_id, receiver_id, status FROM claims WHERE claim_id = %s", (selected_claim,))
                    claim = cursor.fetchone()

                    cursor.execute("SELECT food_id FROM food_listings")
                    food_ids = [row[0] for row in cursor.fetchall()]

                    cursor.execute("SELECT receiver_id FROM receivers")
                    receiver_ids = [row[0] for row in cursor.fetchall()]

                    food_id = st.selectbox("Select Food ID", food_ids, index=food_ids.index(claim[0]))
                    receiver_id = st.selectbox("Select Receiver ID", receiver_ids, index=receiver_ids.index(claim[1]))
                    status = st.selectbox("Status", ["Pending", "Cancelled", "Completed"], index=["Pending", "Cancelled", "Completed"].index(claim[2]))

                    if st.button("Update Claim"):
                        try:
                            cursor.execute("""
                                UPDATE claims SET food_id = %s, receiver_id = %s, status = %s
                                WHERE claim_id = %s
                            """, (food_id, receiver_id, status, selected_claim))
                            conn.commit()
                            st.success(" Claim updated successfully.")
                        except Error as e:
                            st.error(f" Failed to update claim: {e}")
                else:
                    st.warning("No claims found to update.")

            if operation == "Add":
                st.subheader("Add New Claim")

        
                cursor.execute("SELECT food_id FROM food_listings")
                food_ids = [row[0] for row in cursor.fetchall()]

                cursor.execute("SELECT receiver_id FROM receivers")
                receiver_ids = [row[0] for row in cursor.fetchall()]

                food_id = st.selectbox("Select Food ID", food_ids)
                receiver_id = st.selectbox("Select Receiver ID", receiver_ids)
                status = st.selectbox("Status", ["Pending", "Cancelled", "Completed"])
                timestamp = datetime.datetime.now()

                if st.button("Add Claim"):
                    try:
                        cursor.execute("""
                            INSERT INTO claims (food_id, receiver_id, status, timestamp)
                            VALUES (%s, %s, %s, %s)
                        """, (food_id, receiver_id, status, timestamp))
                        conn.commit()
                        st.success(" Claim added successfully.")
                    except Error as e:
                        st.error(f" Failed to add claim: {e}")

            elif operation == "View":
                st.subheader("View Claim Details")

                try:
                    cursor.execute("SELECT claim_id FROM Claims")
                    claim_ids = [row[0] for row in cursor.fetchall()]
                except Error as e:
                    st.error(f"Error fetching claim IDs: {e}")
                    claim_ids = []

                if claim_ids:
                    selected_id = st.selectbox("Select Claim ID to view", claim_ids)

                    try:
                        cursor.execute("""
                            SELECT claim_id, food_id, receiver_id, status, timestamp
                            FROM Claims WHERE claim_id = %s
                        """, (selected_id,))
                        record = cursor.fetchone()

                        if record:
                            st.markdown("### Claim Information")
                            st.write(f"**Claim ID:** {record[0]}")
                            st.write(f"**Food ID:** {record[1]}")
                            st.write(f"**Receiver ID:** {record[2]}")
                            st.write(f"**Status:** {record[3]}")
                            st.write(f"**Timestamp:** {record[4]}")
                        else:
                            st.warning("No data found for this Claim ID.")
                    except Error as e:
                        st.error(f"Error retrieving claim details: {e}")
                else:
                    st.warning("No claim records found.")

            
            elif operation == "Delete":
                st.subheader("Delete Claim Record")

                try:
                    cursor.execute("SELECT claim_id FROM claims")
                    claim_ids = [row[0] for row in cursor.fetchall()]
                except Error as e:
                    st.error(f"Error fetching claim IDs: {e}")
                    claim_ids = []

                if claim_ids:
                    selected_id = st.selectbox("Select Claim ID to delete", claim_ids)

                    if st.button("Delete Claim"):
                        try:
                            cursor.execute("DELETE FROM claims WHERE claim_id = %s", (selected_id,))
                            conn.commit()
                            st.success(f" Claim ID {selected_id} deleted successfully!")
                        except Error as e:
                            st.error(f" Failed to delete claim: {e}")
                else:
                    st.warning("No claim records found to delete.")


elif page == "📊 SQL Queries and Visualisation":
        st.header("📊 SQL Queries and Visualisation")

        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root@123",
        database="food_management"
        )
        
        cursor = conn.cursor()

        questions = {
        "Number of Providers In Each City": """
            select City,count(Provider_ID) as Total_Count from providers group by City order by count(Provider_ID)
        """, 
        "Number of Receivers In Each City": """
        select City,count(Receiver_ID) as Total_Count from receivers group by City order by count(Receiver_ID) """,

        "Food provider that has contributed the most food":"""
        select provider_type,count(quantity) as Quantity from food_listings group by provider_type order by Quantity desc limit 1;""",

        "Total Quantity of Food by each provider":"""
        select provider_id as ID,sum(quantity) as Quantity from food_listings group by provider_id; """,

        "Meal Type which is claimed the most": """
        SELECT food_listings.meal_type, COUNT(claims.claim_id) AS total
        FROM claims
        JOIN food_listings ON food_listings.food_id = claims.food_id
        GROUP BY food_listings.meal_type
        ORDER BY total DESC
        LIMIT 1;
        """,
        "Average quantity of food consumed per receiver":"""
        SELECT 
        SUM(food_listings.quantity) AS total_quantity,
        COUNT(claims.receiver_id) AS total_receivers,
        (SUM(food_listings.quantity) / COUNT(claims.receiver_id)) AS average_quantity_per_receiver
        FROM food_listings
        JOIN claims ON food_listings.food_id = claims.food_id;
        
        """,
        "Percentage of food claims are completed vs. pending vs. canceled":"""
        select status,count(*) as Count,ROUND( (COUNT(*) * 100.0) / (SELECT COUNT(*) FROM claims),2) as Percentage from claims group by status;""",

        "Provider who has the highest number of successful food claims": """
        SELECT 
        food_listings.provider_id,
        COUNT(claims.claim_id) AS total_claims
        FROM claims
        JOIN food_listings ON food_listings.food_id = claims.food_id
        WHERE claims.status = 'completed'
        GROUP BY food_listings.provider_id
        ORDER BY total_claims DESC
        LIMIT 1;
        """,
        "Food claims made for each food item":"""
        SELECT 
        food_listings.food_name,
        COUNT(claims.claim_id) AS total_claims
        FROM food_listings
        JOIN claims ON claims.food_id = food_listings.food_id
        GROUP BY food_listings.food_name
        ORDER BY total_claims DESC;
        """,

        "The most commonly available food types": """
        SELECT 
        food_type, 
        COUNT(*) AS total_count
        FROM food_listings
        GROUP BY food_type
        ORDER BY total_count DESC;
        """,

        "City with the highest number of food listings": """
        SELECT 
        location, 
        COUNT(*) AS total_listings
        FROM food_listings
        GROUP BY location
        ORDER BY total_listings desc limit 1;
        """,

        "Total quantity of food available from all providers": """
        select sum(quantity) from food_listings;""",

        "Receivers who have claimed the most food": """
        SELECT 
        receivers.Receiver_ID,
        receivers.Name AS receiver_name,
        COUNT(claims.Claim_ID) AS total_completed_claims
        FROM claims
        JOIN receivers ON receivers.Receiver_ID = claims.Receiver_ID
        WHERE claims.Status = 'Completed'
        GROUP BY receivers.Receiver_ID, receivers.Name
        ORDER BY total_completed_claims DESC
        LIMIT 5;
        """,

        "Contact details city wise": """ 
        SELECT city, GROUP_CONCAT(contact SEPARATOR ', ') AS contacts
        FROM providers
        GROUP BY city
        ORDER BY city;"""

        
       
        }



        selected_question = st.selectbox("Select a question :", list(questions.keys()))
        df = pd.read_sql(
        questions[selected_question],
        conn
        )

        st.markdown("### Query Result")
        st.dataframe(df)

        if selected_question == "Number of Providers In Each City":
            st.subheader("📊 Number of Providers in Each City")

            st.bar_chart(
                data=df,
                x="City",
                y="Total_Count"
            )
        
        elif selected_question == "Number of Receivers In Each City":
            st.subheader("📊 Number of Receivers in Each City")
            st.bar_chart(df, x="City", y="Total_Count")

        elif selected_question == "Food claims made for each food item":
            st.subheader("📊 Food Claims by Food Item")
            st.bar_chart(df, x="food_name", y="total_claims")

        elif selected_question == "The most commonly available food types":
            st.subheader("📊 Most Commonly Available Food Types")
            st.bar_chart(df, x="food_type", y="total_count")

        elif selected_question == "Percentage of food claims are completed vs. pending vs. canceled":
            st.subheader("📊 Claim Status Distribution")
            st.bar_chart(df, x="status", y="Percentage")

    
elif page == "🧠 Learner SQL Queries":
        st.header("Learner SQL Queries")
        conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root@123",
        database="food_management"
        )
        
        cursor = conn.cursor()


        learner_questions = [
        
        "Sum of quantity based on type of providers",
        "List expired food items",
        "Receivers of each type (NGO, Community Center, Individual)",
        "Total quantity donated by each provider",
        "Cities that have active food listings with provider names",
        "Receivers and the types of meals they have claimed",
        "Count of completed claims"
        
        ]

        selected_query = st.selectbox("Select a learner SQL question:", learner_questions)

        if selected_query == "List expired food items":
            query = """
            SELECT food_id, food_name, expiry_date
            FROM food_listings
            WHERE expiry_date < '2025-03-20'
            """

            df = pd.read_sql(query, conn)

            st.markdown("### Query Results")
            st.dataframe(df)



            st.markdown("Expired Items by Food Name graph")
            expired_counts = df['food_name'].value_counts().reset_index()
            expired_counts.columns = ['food_name', 'count']
            st.bar_chart(expired_counts.set_index('food_name'))

        elif selected_query == "Sum of quantity based on type of providers":
        
            query=("""
            SELECT providers.type AS provider_type,
            SUM(food_listings.quantity) AS total_quantity
            FROM providers 
            JOIN food_listings ON providers.provider_id = food_listings.provider_id
            GROUP BY providers.type
            ORDER BY total_quantity DESC
            """)  

            df=pd.read_sql(query,conn)

            st.markdown("### Query Results")
            st.dataframe(df)
            
        
        elif selected_query == "Receivers of each type (NGO, Community Center, Individual)":
            query = """
                SELECT type, COUNT(*) AS total
                FROM receivers
                GROUP BY type;
            """

            df = pd.read_sql(query, conn)

            st.markdown("Query Results")
            st.dataframe(df)
            st.bar_chart(df.set_index("type"))



        elif selected_query == "Total quantity donated by each provider":
            query = """
                SELECT provider_id, SUM(quantity) AS total_quantity
                FROM food_listings
                GROUP BY provider_id;
            """

            df = pd.read_sql(query, conn)

            st.markdown("Query Results")
            st.dataframe(df)


               
            

        elif selected_query == "Cities that have active food listings with provider names":
            query = """
                SELECT 
                    food_listings.food_name,
                    providers.name AS provider_name,
                    food_listings.location
                FROM food_listings
                JOIN providers ON food_listings.provider_id = providers.provider_id;
            """

            df = pd.read_sql(query, conn)

            st.markdown("Query Results")
            st.dataframe(df)

        elif selected_query == "Receivers and the types of meals they have claimed":
            query = """
                SELECT 
                    receivers.name AS receiver_name,
                    food_listings.meal_type
                FROM claims
                JOIN receivers ON claims.receiver_id = receivers.receiver_id
                JOIN food_listings ON claims.food_id = food_listings.food_id;
            """

            df = pd.read_sql(query, conn)

            st.markdown("Query Results")
            st.dataframe(df)


        elif selected_query == "Count of completed claims":
            cursor.execute("""
            SELECT COUNT(*) AS completed_claims_count
            FROM claims
            WHERE status = 'Completed';
            """)  

            result = cursor.fetchone() 
            df = pd.DataFrame([result], columns=['Completed Claims'])

            
            st.dataframe(df)

            st.metric("Completed Claims", result[0])


elif page == "👤 User Introduction":
        st.write("## ABOUT:")
        st.write("Name : Avanthi U C")
        st.markdown("Course: Data Science")


elif page == "🔍 Find Info":
    st.set_page_config(layout="centered")

    st.title(" Search Data by Column")

    conn = mysql.connector.connect(
    host="localhost",
     user="root",
    password="root@123",
    database="food_management"
    )

    # Select Table
    table = st.selectbox(
    "Select Table",
    ["food_listings", "providers", "receivers", "claims"]
)


    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query, conn)

    #Select Column
    column = st.selectbox("Select Column", df.columns)

    #Search input
    search_value = st.text_input(
        f"Enter value to search in '{column}'"
        )

    if search_value:
        filtered_df = df[
        df[column]
        .astype(str)
        .str.contains(search_value, case=False, na=False)
        ]

        st.success("Found Records:")
        st.dataframe(filtered_df)
    else:
        st.info("Select a column and enter a value")

               
           
            
        




    

        


        

    

                

            










        
           
       
        

        
        

        


