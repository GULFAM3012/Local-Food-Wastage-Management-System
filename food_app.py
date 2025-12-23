import streamlit as st
import mysql.connector 
import pandas as pd
from datetime import datetime

def connect_to_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tigerx@007",
        database="food_data"
    )
    return conn

def run_query(query):
    conn = connect_to_database()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def fetch_data(conn, query):
    return pd.read_sql(query, conn)

def execute_query(conn, query, values):
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    return True

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go To", [
    "Project Introduction", "View Table", "CRUD Operations", 
    "SQL Queries & Visualization", "My SQL Queries", "Provider Contacts"
])

if page == "Project Introduction":
    st.title("🍴 Local Food Waste Management System")
    st.write(""" 
This project addresses the problem of food wastage. Every day, restaurants, grocery stores, and households throw away surplus food, while many people struggle with food insecurity.

The system aims to connect food providers (restaurants, stores, individuals) with receivers (NGOs, community centers, needy individuals) through a digital platform.

**⚙️ How it Works**

SQL Database stores details of providers, receivers, food items, and claims.

Streamlit Application allows users to:

View and filter food listings by city, type, or provider

Perform CRUD operations (Create, Read, Update, Delete)

Access contact details for direct coordination

Data Analysis helps identify food wastage trends and improve food distribution.

**🌍 Social Impact**

Reduces food waste effectively

Ensures surplus food reaches people in need

Promotes sustainability and community well-being
""")

elif page == "View Table":
    st.title("Database Tables")
    conn = connect_to_database()
    table_name = st.selectbox("Select Table", ["providers", "receivers", "food_listings", "claims"])
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql(query, conn)
    st.dataframe(df)
    conn.close()

elif page == "CRUD Operations":
    st.title("CRUD Operations")
    conn = connect_to_database()
    table_name = st.selectbox("Select Table", ["providers", "receivers", "food_listings", "claims"])

    if table_name == "providers":
        operation_name = st.selectbox("Select Action", 
            ["Add New Provider", "Update Provider", "Delete Provider"])

        if operation_name == "Add New Provider":
            st.subheader("Add New Provider")
            with st.form("add_provider_form"):
                provider_id = st.number_input("Provider ID", min_value=1)
                name = st.text_input("Provider Name")
                provider_type = st.selectbox("Type", ["Restaurant", "Grocery Store", "Supermarket"])
                address = st.text_input("Address")
                city = st.text_input("City")
                contact = st.text_input("Contact Number")
                submitted = st.form_submit_button("Add Provider")
                if submitted:
                    cursor = conn.cursor()
                    query = "INSERT INTO providers VALUES (%s,%s,%s,%s,%s,%s)"
                    cursor.execute(query, (provider_id, name, provider_type, address, city, contact))
                    conn.commit()
                    st.success("Provider added successfully!")

        elif operation_name == "Update Provider":
            st.subheader("Update Provider")
            with st.form("Update_Provider"):
                provider_id = st.number_input("Enter Provider ID to Update", min_value=1)
                new_name = st.text_input("New Provider Name")
                new_contact = st.text_input("New Contact Number")
                submitted = st.form_submit_button("Update Provider")
                if submitted:
                    cursor = conn.cursor()
                    query = "UPDATE providers SET NAME=%s, CONTACT=%s WHERE Provider_Id=%s"
                    cursor.execute(query,(new_name, new_contact, provider_id))
                    conn.commit()
                    st.success(f"Provider ID {provider_id} updated successfully!")

        elif operation_name == "Delete Provider":
            st.subheader("Delete Provider")
            with st.form("delete_provider"):
                provider_id = st.number_input("Provider ID to Delete", min_value=1)
                submitted = st.form_submit_button("Delete Provider")
                if submitted:
                    cursor = conn.cursor()
                    query = "DELETE FROM providers WHERE Provider_Id=%s"
                    cursor.execute(query, (provider_id, ))
                    conn.commit()
                    st.success("Provider Deleted")

    elif table_name == "receivers":
        operation_name = st.selectbox("Select Action", 
            ["Add New Receiver", "Update Receiver", "Delete Receiver"])

        if operation_name == "Add New Receiver":
            st.subheader("Add New Receiver")
            with st.form("add_receiver_form"):
                receiver_id = st.number_input("Receiver Id", min_value=1)
                name = st.text_input("Receiver Name")
                receiver_type = st.selectbox("Type", ["NGO", "Community Center", "Individual"])
                city = st.text_input("City")
                contact = st.text_input("Contact Number")
                submitted = st.form_submit_button("Add Receiver")
                if submitted:
                    cursor = conn.cursor()
                    query = "INSERT INTO receivers VALUES (%s,%s,%s,%s,%s)"
                    cursor.execute(query, (receiver_id, name, receiver_type, city, contact))
                    conn.commit()
                    st.success("Receiver added successfully!")

        elif operation_name == "Update Receiver":
            st.subheader("Update Receiver")
            with st.form("update_receiver_form"):
                receiver_id = st.number_input("Enter Receiver Id to Update", min_value=1)
                new_name = st.text_input("New Receiver Name")
                new_city = st.text_input("New City")
                new_contact = st.text_input("New Contact Number")
                submitted = st.form_submit_button("Update Receiver")
                if submitted:
                    cursor = conn.cursor()
                    query = "UPDATE receivers SET NAME=%s, CITY=%s, CONTACT=%s WHERE Receivers_Id=%s"
                    cursor.execute(query, (new_name, new_city, new_contact, receiver_id))
                    conn.commit()
                    st.success(f"Receiver {receiver_id} Update Successfully")

        elif operation_name == "Delete Receiver":
            st.subheader("Delete Receiver")
            with st.form("Delete_Receiver"):
                receiver_id = st.number_input("Receiver ID to Delete", min_value=1)
                submitted = st.form_submit_button("Delete Receiver")
                if submitted:
                    cursor = conn.cursor()
                    query = "DELETE FROM receivers WHERE Receivers_Id=%s"
                    cursor.execute(query, (receiver_id, ))
                    conn.commit()
                    st.success("Receiver Deleted")

    elif table_name == "food_listings":
        operation_name = st.selectbox("Select Action", 
            ["Add New Food", "Update Food", "Delete Food"])

        if operation_name == "Add New Food":
            st.subheader("Add New Food")
            with st.form("add_food_listing_form"):
                food_id = st.number_input("Food Id", min_value=1)
                food_name = st.text_input("FOOD NAME")
                quantity = st.number_input("FOOD QUANTITY", min_value=1)
                expiry_date = st.date_input("Select Expiry_Date")
                provider_id = st.number_input("PROVIDER_ID", min_value=1)
                provider_type = st.selectbox("PROVIDER_TYPE",["Restaurant", "Grocery Store", "Supermarket"])
                location = st.text_input("LOCATION")
                food_type = st.selectbox("FOOD_TYPE",["Vegetarian", "Non-Vegetarian", "Vegan"])
                meal_type = st.selectbox("MEAL_TYPE",["Breakfast", "Lunch", "Dinner", "Snacks"])
                submitted = st.form_submit_button("Add New Food")
                if submitted:
                    cursor = conn.cursor()
                    query = "INSERT INTO food_listings VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(query, (food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type))
                    conn.commit()
                    st.success("New Food added successfully!")

        elif operation_name == "Update Food":
            st.subheader("Update Food")
            food_id = st.number_input("Enter Food Id to Update", min_value=1, key="update_food_id")

            if st.button("Check Current Details", key="check_button"):
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM food_listings WHERE Food_Id = %s", (food_id,))
                food_data = cursor.fetchone()

                if food_data:
                    st.session_state['food_to_update'] = {
                        'food_id': food_data[0],
                        'food_name': food_data[1],
                        'quantity': food_data[2],
                        'expiry_date': food_data[3],
                        'provider_id': food_data[4],
                        'provider_type': food_data[5],
                        'location': food_data[6],
                        'food_type': food_data[7],
                        'meal_type': food_data[8]
                    }
                    st.success("Current Food Details:")
                else:
                    st.error("Food ID not found!")


            if 'food_to_update' in st.session_state:
                food_data = st.session_state['food_to_update']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.text_input("Food Name", value=food_data['food_name'], disabled=True, key="curr_name")
                    st.text_input("Provider Type", value=food_data['provider_type'], disabled=True, key="curr_provider_type")
                with col2:
                    st.text_input("Current Quantity", value=food_data['quantity'], disabled=True, key="curr_qty")
                    st.text_input("Provider ID", value=food_data['provider_id'], disabled=True, key="curr_provider_id")
                with col3:
                    st.text_input("Current Expiry", value=str(food_data['expiry_date']), disabled=True, key="curr_expiry")
                    st.text_input("Location", value=food_data['location'], disabled=True, key="curr_location")


                with st.form("update_food_values_form"):
                    st.subheader("Enter New Values:")
                    new_quantity = st.number_input("New Quantity", min_value=0, value=int(food_data['quantity']),key="new_qty")
                    new_expiry = st.date_input("New Expiry Date", value=pd.to_datetime(food_data['expiry_date']),key="new_expiry")
                    new_food_type = st.selectbox("New Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"],index=["Vegetarian", "Non-Vegetarian", "Vegan"].index(food_data['food_type']),key="new_food_type")
                    new_meal_type = st.selectbox("New Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"],index=["Breakfast", "Lunch", "Dinner", "Snacks"].index(food_data['meal_type']),key="new_meal_type")

                    update_submitted = st.form_submit_button("Update Food")

                    if update_submitted:
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE food_listings SET QUANTITY=%s, EXPIRY_DATE=%s, FOOD_TYPE=%s, MEAL_TYPE=%s WHERE Food_Id=%s",
                            (new_quantity, new_expiry, new_food_type, new_meal_type, food_data['food_id'])
                        )
                        conn.commit()
                        st.success(f" Food ID {food_data['food_id']} updated successfully!")
                        del st.session_state['food_to_update']
                    else:
                        st.error("Food ID not found!")

        elif operation_name == "Delete Food":
            st.subheader("Delete food")
            with st.form("Delete_Food"):
                food_id = st.number_input("Food ID to Delete", min_value=1)
                submitted = st.form_submit_button("Delete Food")
                if submitted:
                    cursor = conn.cursor()
                    query = "DELETE FROM food_listings WHERE Food_Id=%s"
                    cursor.execute(query, (food_id, ))
                    conn.commit()
                    st.success("Food Deleted")
                else:
                    st.error("Food ID not found!")



    elif table_name == "claims":
        operation_name = st.selectbox("Select Action", 
            ["Add New Claim", "Update Claim", "Delete Claim"])

        if operation_name == "Add New Claim":
            st.subheader("Add New Claim")
            cursor = conn.cursor()
            cursor.execute("SELECT Food_Id, FOOD_NAME FROM food_listings")
            food_items = cursor.fetchall()
            cursor.execute("SELECT Receivers_Id, NAME FROM receivers")
            receivers = cursor.fetchall()
            with st.form("add_claim_form"):
                food_option = st.selectbox("Select Food", options=[f"{f[0]} - {f[1]}" for f in food_items])
                receiver_option = st.selectbox("Select Receiver", options=[f"{r[0]} - {r[1]}" for r in receivers])
                claim_quantity = st.number_input("Claim Quantity", min_value=1)
                status = st.selectbox("Status", ["Pending", "Successful", "Failed"])
                submitted = st.form_submit_button("Add Claim")
                if submitted:
                    food_id_val = int(food_option.split(' - ')[0])
                    receiver_id_val = int(receiver_option.split(' - ')[0])
                    cursor.execute("SELECT QUANTITY FROM food_listings WHERE Food_Id = %s", (food_id_val,))
                    current_qty = int(cursor.fetchone()[0])

                    if claim_quantity > current_qty:
                        st.error(f"Not enough quantity! Available: {current_qty}")
                    else:
                        cursor.execute("SELECT MAX(Claim_Id) FROM claims")
                        max_id = cursor.fetchone()[0]
                        new_claim_id = 1 if max_id is None else max_id + 1
                        query = "INSERT INTO claims (Claim_Id, Food_Id, Receivers_Id, STATUS, TIMESTAMP) VALUES (%s, %s, %s, %s, %s)"
                        cursor.execute(query, (new_claim_id, food_id_val, receiver_id_val, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

                        if status == "Successful":
                            #cursor.execute("""UPDATE food_listings SET QUANTITY = CAST(QUANTITY AS UNSIGNED) - 1 WHERE Food_Id = %s""", (food_id_val,))
                            new_qty = current_qty - claim_quantity
                            cursor.execute("UPDATE food_listings SET QUANTITY=%s WHERE Food_Id=%s",(new_qty, food_id_val)) 

                        conn.commit()
                        st.success("Claim added successfully!")


        elif operation_name == "Update Claim":
            st.subheader("Update Claim Status")
            with st.form("update_claim_form"):
                claim_id = st.number_input("Claim ID to Update", min_value=1)
                new_status = st.selectbox("New Status", ["Pending", "Successful", "Failed"])
                submitted = st.form_submit_button("Update Claim")
                if submitted:
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM claims WHERE Claim_Id = %s", (claim_id,))
                    claim_exists = cursor.fetchone()[0]
                    if claim_exists > 0:
                        query = "UPDATE claims SET STATUS=%s WHERE Claim_Id=%s"
                        cursor.execute(query, (new_status, claim_id))
                        conn.commit()
                        st.success(f"Claim {claim_id} updated successfully!")
                    else:
                        st.error("Claim ID not found!")


        elif operation_name == "Delete Claim":
            st.subheader("Delete Claim")
            with st.form("delete_claim_form"):
                claim_id = st.number_input("Claim ID to Delete", min_value=1)
                submitted = st.form_submit_button("Delete Claim")
                if submitted:
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM claims WHERE Claim_Id = %s", (claim_id,))
                    claim_exists = cursor.fetchone()[0]

                    if claim_exists > 0:
                        query = "DELETE FROM claims WHERE Claim_Id=%s"
                        cursor.execute(query, (claim_id,))
                        conn.commit()
                        st.success("Claim deleted successfully!")
                    else:
                        st.error("Claim ID not found!")


    conn.close()

elif page == "SQL Queries & Visualization":
    st.title("📊 SQL Queries & Visualization")
    all_queries = {
        "1. Providers per City": "SELECT CITY, COUNT(*) as Total_Providers FROM providers GROUP BY CITY",
        "2. Receivers per City": "SELECT CITY, COUNT(*) as Total_Receivers FROM receivers GROUP BY CITY",
        "3. Type of provider contributing most": "SELECT PROVIDER_TYPE, SUM(QUANTITY) as Total_Quantity_Contributed FROM food_listings GROUP BY PROVIDER_TYPE ORDER BY Total_Quantity_Contributed DESC LIMIT 1;",
        "4. Contact info of providers in a specific city": "SELECT Name, Contact FROM providers WHERE City = 'New Jessica'",
        "5. Top Receivers by Claims": "SELECT r.NAME, COUNT(c.Claim_Id) as Total_Claims FROM claims c JOIN receivers r ON c.Receivers_Id = r.Receivers_Id GROUP BY r.NAME ORDER BY Total_Claims DESC LIMIT 10",
        "6. Total Food Available": "SELECT SUM(QUANTITY) as Total_Food_Available FROM food_listings",
        "7. City with Most Listings": "SELECT LOCATION, COUNT(*) as Listings FROM food_listings GROUP BY LOCATION ORDER BY Listings DESC LIMIT 5",
        "8. Most Common Food Types": "SELECT FOOD_TYPE, COUNT(*) as Count FROM food_listings GROUP BY FOOD_TYPE ORDER BY Count DESC",
        "9. Claims per Food Item": "SELECT f.FOOD_NAME, COUNT(c.Claim_Id) as Claims FROM claims c JOIN food_listings f ON c.Food_Id = f.Food_Id GROUP BY f.FOOD_NAME ORDER BY Claims DESC LIMIT 10",
        "10. Providers with highest Successful Claims": "SELECT p.Name, COUNT(*) as Successful_Claims FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID JOIN providers p ON f.Provider_ID = p.Provider_ID WHERE Status = 'Completed' GROUP BY p.Name ORDER BY Successful_Claims DESC LIMIT 1",
        "11. Claim Status Distribution": "SELECT STATUS, COUNT(*) as Count, ROUND((COUNT(*)*100.0/(SELECT COUNT(*) FROM claims)),2) as Percentage FROM claims GROUP BY STATUS",
        "12. Avg quantity claimed per receiver": "SELECT r.Name, AVG(f.Quantity) as Avg_Quantity FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID JOIN receivers r ON c.Receivers_ID = r.Receivers_ID GROUP BY r.Name",
        "13. Most Claimed Meal Type": "SELECT MEAL_TYPE, COUNT(c.Claim_Id) as Claims FROM claims c JOIN food_listings f ON c.Food_Id = f.Food_Id GROUP BY MEAL_TYPE ORDER BY Claims DESC",
        "14. Food Donated by Each Provider": "SELECT p.Name, SUM(f.Quantity) as Total_Donated FROM food_listings f JOIN providers p ON f.Provider_ID = p.Provider_ID GROUP BY p.Name ORDER BY Total_Donated DESC"
    }

    selected_query = st.selectbox("Select Query to Execute", list(all_queries.keys()))

    if st.button("Run Selected Query"):
        query = all_queries[selected_query]
        df = run_query(query)

        st.subheader(f"Results: {selected_query}")
        st.dataframe(df, use_container_width=True)


        with st.expander("View SQL Query"):
            st.code(query, language='sql')


        if len(df) > 1 and len(df.columns) == 2:
            st.subheader("Visualization")
            chart_data = df.set_index(df.columns[0])
            st.bar_chart(chart_data)

elif page == "My SQL Queries":
    st.title("My SQL Queries")
    all_queries = {
        "1. Top Receivers by Claims": "SELECT r.NAME, COUNT(c.Claim_Id) as Total_Claims FROM claims c JOIN receivers r ON c.Receivers_Id = r.Receivers_Id GROUP BY r.NAME ORDER BY Total_Claims DESC LIMIT 10",
        "2. Total pendind Claims": "SELECT COUNT(*) AS Pending_Claims FROM claims WHERE STATUS = 'Pending'",
        "3. City-wise average food quantity": "SELECT LOCATION, AVG(QUANTITY) AS Average_Quantity FROM food_listings GROUP BY LOCATION",
        "4. Expired food count": "SELECT COUNT(*) AS Expired_Food_Count FROM food_listings WHERE EXPIRY_DATE < CURDATE()",
        "5. Expiring Soon Food": "SELECT FOOD_NAME, EXPIRY_DATE, QUANTITY, LOCATION FROM food_listings WHERE EXPIRY_DATE >= CURDATE() ORDER BY EXPIRY_DATE LIMIT 10"
    }

    selected_query = st.selectbox("Select Query to Execute", list(all_queries.keys()))

    if st.button("Run Selected Query"):
        query = all_queries[selected_query]
        df = run_query(query)

        st.subheader(f"Results: {selected_query}")
        st.dataframe(df, use_container_width=True)


        with st.expander("View SQL Query"):
            st.code(query, language='sql')


        if len(df) > 1 and len(df.columns) == 2:
            st.subheader("Visualization")
            chart_data = df.set_index(df.columns[0])
            st.bar_chart(chart_data)

elif page == "Provider Contacts":
    st.title("📞 Provider Contact List")
    conn = connect_to_database()
    query = "SELECT Name, Type, City, Contact FROM providers;"
    df = pd.read_sql(query, conn)
    st.dataframe(df)
    conn.close()
