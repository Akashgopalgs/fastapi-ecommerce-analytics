import streamlit as st
import requests
import pandas as pd
from datetime import date

# =========================
# BASIC CONFIG
# =========================
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    layout="wide",
)

st.title("📊 E-commerce Sales Dashboard")

# =========================
# API BASE URL (SIDEBAR)
# =========================
st.sidebar.header("API Settings")

# Change this if your FastAPI runs elsewhere
BASE_URL = st.sidebar.text_input(
    "FastAPI base URL",
    "http://localhost:8000",
).rstrip("/")


# =========================
# HELPER: API REQUEST WRAPPER
# =========================
def handle_request(method: str, endpoint: str, base_url: str, **kwargs):
    """Generic request wrapper with basic error handling."""
    url = f"{base_url}{endpoint}"
    try:
        resp = requests.request(method=method, url=url, timeout=15, **kwargs)
    except Exception as e:
        st.error(f"Request failed: {e}")
        return None

    if not resp.ok:
        st.error(f"API error [{resp.status_code}]: {resp.text}")
        return None

    try:
        return resp.json()
    except ValueError:
        st.error("Failed to parse JSON response.")
        return None


# =========================
# BACKEND HEALTH CHECK
# =========================
def check_backend(base_url: str):
    return handle_request("GET", "/", base_url)


backend_msg = check_backend(BASE_URL)

if backend_msg is None:
    st.warning(
        "Could not connect to the FastAPI backend. "
        "Make sure it is running on the URL shown in the sidebar."
    )
else:
    st.success(f"Connected to backend ✅  Message: {backend_msg}")


# =========================
# API CALL HELPERS
# =========================
@st.cache_data(show_spinner=False)
def get_all_products(base_url: str):
    return handle_request("GET", "/products/", base_url)


def search_products_by_name(keyword: str, base_url: str):
    return handle_request("GET", f"/products/search/{keyword}", base_url)


def filter_products_by_category(word: str, base_url: str):
    return handle_request("GET", f"/products/filter/{word}", base_url)


def filter_products_by_date_range(from_dt: date, to_dt: date, base_url: str):
    # Backend expects YYYY-MM-DD strings in path
    return handle_request(
        "GET",
        f"/products/filter/{from_dt.isoformat()}/{to_dt.isoformat()}",
        base_url,
    )


def filter_products_by_price(min_price: float, max_price: float, base_url: str):
    # Your backend route: /products/filter/price/{max_price}/{min_price}
    return handle_request(
        "GET",
        f"/products/filter/price/{max_price}/{min_price}",
        base_url,
    )


@st.cache_data(show_spinner=False)
def get_customers_by_location(base_url: str):
    return handle_request("GET", "/customer/user", base_url)


@st.cache_data(show_spinner=False)
def get_top_customers_by_orders(base_url: str):
    return handle_request("GET", "/customer/mostorder", base_url)


def trigger_load_products(base_url: str):
    return handle_request("POST", "/load-products", base_url)


# =========================
# SIDEBAR: PAGE SELECTION
# =========================
st.sidebar.markdown("### Views")
page = st.sidebar.radio(
    "Select view",
    [
        "Overview",
        "Products: Browse & Filter",
        "Customer Analytics",
        "Admin: Load CSV to DB",
    ],
)

# =========================
# PAGE 1: OVERVIEW
# =========================
if page == "Overview":
    st.subheader("Overview")

    products = get_all_products(BASE_URL)

    if not products:
        st.info("No products returned. Make sure the API is running and the DB has data.")
    else:
        df = pd.DataFrame(products)

        required_cols = {
            "id",
            "date",
            "name",
            "category",
            "price",
            "quantity",
            "total_sales",
            "customer_name",
            "customer_location",
            "payment_method",
            "status",
        }
        missing = required_cols - set(df.columns)
        if missing:
            st.warning(f"Missing columns in response: {missing}")

        # Convert date column to datetime if present
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])

        # KPI cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Orders", len(df))

        with col2:
            if "total_sales" in df.columns:
                st.metric(
                    "Total Sales (sum of total_sales)",
                    int(df["total_sales"].sum()),
                )
            else:
                st.metric("Total Sales", "N/A")

        with col3:
            if "price" in df.columns:
                st.metric(
                    "Average Price",
                    round(float(df["price"].mean()), 2),
                )
            else:
                st.metric("Average Price", "N/A")

        with col4:
            if "customer_name" in df.columns:
                st.metric("Unique Customers", df["customer_name"].nunique())
            else:
                st.metric("Unique Customers", "N/A")

        st.markdown("### Recent Orders")
        if "date" in df.columns:
            df_sorted = df.sort_values("date", ascending=False)
        else:
            df_sorted = df
        st.dataframe(df_sorted.head(50), use_container_width=True)


# =========================
# PAGE 2: PRODUCTS – BROWSE & FILTER
# =========================
elif page == "Products: Browse & Filter":
    st.subheader("Products – Browse & Filter")

    tab_all, tab_search, tab_category, tab_date, tab_price = st.tabs(
        ["All Products", "Search by Name", "Filter by Category", "Filter by Date", "Filter by Price"]
    )

    # ---- All Products ----
    with tab_all:
        st.markdown("#### All Products")
        products = get_all_products(BASE_URL)
        if products:
            df = pd.DataFrame(products)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No products found.")

    # ---- Search by Name ----
    with tab_search:
        st.markdown("#### Search by Product Name")
        keyword = st.text_input("Enter product keyword")
        if st.button("Search", key="search_name_btn"):
            if keyword.strip():
                data = search_products_by_name(keyword.strip(), BASE_URL)
                if data:
                    df = pd.DataFrame(data)
                    st.success(f"Found {len(df)} matching products.")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No products matched that keyword.")
            else:
                st.warning("Please enter a keyword.")

    # ---- Filter by Category ----
    with tab_category:
        st.markdown("#### Filter by Category Keyword")
        cat_word = st.text_input(
            "Enter category keyword (e.g. 'Electronics', 'Clothing')"
        )
        if st.button("Filter by Category"):
            if cat_word.strip():
                data = filter_products_by_category(cat_word.strip(), BASE_URL)
                if data:
                    df = pd.DataFrame(data)
                    st.success(
                        f"Found {len(df)} products in category matching '{cat_word}'."
                    )
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No products found for that category keyword.")
            else:
                st.warning("Please enter a keyword.")

    # ---- Filter by Date ----
    with tab_date:
        st.markdown("#### Filter by Date Range")

        col1, col2 = st.columns(2)
        with col1:
            from_date = st.date_input("From date", value=date(2025, 1, 1))
        with col2:
            to_date = st.date_input("To date", value=date(2025, 12, 31))

        if st.button("Filter by Date Range"):
            if from_date > to_date:
                st.warning("From date cannot be after To date.")
            else:
                data = filter_products_by_date_range(from_date, to_date, BASE_URL)
                if data:
                    df = pd.DataFrame(data)
                    st.success(
                        f"Found {len(df)} products between {from_date} and {to_date}."
                    )
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No products found in that date range.")

    # ---- Filter by Price ----
    with tab_price:
        st.markdown("#### Filter by Price Range")

        min_price = st.number_input(
            "Minimum price", min_value=0.0, value=0.0, step=1.0
        )
        max_price = st.number_input(
            "Maximum price", min_value=0.0, value=1000.0, step=1.0
        )

        if st.button("Filter by Price"):
            if min_price > max_price:
                st.warning("Minimum price cannot be greater than maximum price.")
            else:
                data = filter_products_by_price(min_price, max_price, BASE_URL)
                if data:
                    df = pd.DataFrame(data)
                    st.success(
                        f"Found {len(df)} products in price range {min_price} – {max_price}."
                    )
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No products found in that price range.")


# =========================
# PAGE 3: CUSTOMER ANALYTICS
# =========================
elif page == "Customer Analytics":
    st.subheader("Customer Analytics")

    tab_loc, tab_orders = st.tabs(["By Location", "By Orders"])

    # ---- Customers by Location ----
    with tab_loc:
        st.markdown("#### Customers by Location")
        data = get_customers_by_location(BASE_URL)
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)

            if {"customer_location", "total_customers"} <= set(df.columns):
                st.bar_chart(
                    df.set_index("customer_location")["total_customers"],
                    use_container_width=True,
                )
        else:
            st.info("No customer-location data available.")

    # ---- Customers by Number of Orders ----
    with tab_orders:
        st.markdown("#### Top Customers by Number of Orders")
        data = get_top_customers_by_orders(BASE_URL)
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)

            if {"customer_name", "no_of_orders"} <= set(df.columns):
                st.bar_chart(
                    df.set_index("customer_name")["no_of_orders"],
                    use_container_width=True,
                )
        else:
            st.info("No order-count data available.")


# =========================
# PAGE 4: ADMIN – LOAD CSV
# =========================
elif page == "Admin: Load CSV to DB":
    st.subheader("Admin – Load CSV Data into DB")

    st.markdown(
        """
This will call your FastAPI endpoint **POST /load-products**,  
which reads the CSV from the backend path and inserts rows into the database.
    """
    )

    if st.button("Trigger /load-products"):
        result = trigger_load_products(BASE_URL)
        if result:
            st.success(f"Response: {result}")
        else:
            st.error("Failed to load products. Check logs / backend.")
