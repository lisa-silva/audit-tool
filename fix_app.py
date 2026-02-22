# fix_app.py
import streamlit as st
from schema_fixer import LocalBusinessSchemaGenerator

st.set_page_config(page_title="AgentAir Schema Fixer", layout="centered")

st.title("🛠️ AgentAir AI Visibility Fixer")
st.markdown("Generate proper schema markup to make your business visible to AI search.")

with st.form("schema_form"):
    st.subheader("Business Information")
    
    col1, col2 = st.columns(2)
    with col1:
        business_name = st.text_input("Business Name")
        service_type = st.selectbox(
            "Service Type",
            ["plumber", "roofer", "electrician", "hvac", "general"]
        )
        phone = st.text_input("Phone Number")
    
    with col2:
        url = st.text_input("Website URL")
        email = st.text_input("Email (optional)")
    
    st.subheader("Address")
    street = st.text_input("Street Address")
    city = st.text_input("City")
    
    col3, col4 = st.columns(2)
    with col3:
        state = st.text_input("State", max_chars=2)
    with col4:
        zip_code = st.text_input("ZIP Code")
    
    st.subheader("Hours of Operation (optional)")
    
    hours = {}
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for day in days:
        with st.expander(day):
            col_open, col_close = st.columns(2)
            with col_open:
                open_time = st.time_input(f"{day} Open", value=None, key=f"{day}_open")
            with col_close:
                close_time = st.time_input(f"{day} Close", value=None, key=f"{day}_close")
            
            if open_time and close_time:
                hours[day.lower()] = {
                    "open": open_time.strftime("%H:%M"),
                    "close": close_time.strftime("%H:%M")
                }
    
    submitted = st.form_submit_button("Generate Schema")

if submitted:
    # Build business data
    business_data = {
        "name": business_name,
        "service_type": service_type,
        "phone": phone,
        "url": url,
        "address": {
            "street": street,
            "city": city,
            "state": state.upper(),
            "zip": zip_code
        },
        "hours": hours
    }
    
    # Generate schema
    generator = LocalBusinessSchemaGenerator(business_data)
    html_code = generator.generate_html()
    
    st.success("Schema generated successfully!")
    
    st.subheader("📋 Copy this code")
    st.code(html_code, language="html")
    
    st.info(
        "Paste this code into the `<head>` section of your website, "
        "or use a plugin like 'Insert Headers and Footers' for WordPress."
    )
    
    # Download option
    st.download_button(
        "📥 Download HTML File",
        html_code,
        file_name=f"{business_name.lower().replace(' ', '_')}_schema.html"
    )
