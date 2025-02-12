import streamlit as st
import stripe
import urllib.parse


def get_api_key() -> str:
    testing_mode = st.secrets.get("testing_mode", False)
    return (
        st.secrets["stripe_api_key_test"]
        if testing_mode
        else st.secrets["stripe_api_key"]
    )


def redirect_button(
    text: str,
    customer_email: str,
    color="#FD504D",
    payment_provider: str = "stripe",
    sidebar: bool = True,
):
    testing_mode = st.secrets.get("testing_mode", False)
    encoded_email = urllib.parse.quote(customer_email)
    if payment_provider == "stripe":
        stripe.api_key = get_api_key()
        stripe_link = (
            st.secrets["stripe_link_test"]
            if testing_mode
            else st.secrets["stripe_link"]
        )
        button_url = f"{stripe_link}?prefilled_email={encoded_email}"
    elif payment_provider == "bmac":
        button_url = f"{st.secrets['bmac_link']}"
    else:
        raise ValueError("payment_provider must be 'stripe' or 'bmac'")

    markdown = st.sidebar.markdown if sidebar else st.markdown

    markdown(
        f"""
    <a href="{button_url}" target="_self">
        <div style="
            display: inline-block;
            padding: 0.5em 1em;
            color: #FFFFFF;
            background-color: {color};
            border-radius: 3px;
            text-decoration: none;">
            {text}
        </div>
    </a>
    """,
        unsafe_allow_html=True,
    )


def get_customer(email: str):
    stripe_customer_id = st.session_state.get("stripe_customer_id", None)
    print("get_customer stripe_customer_id", stripe_customer_id)

    if stripe_customer_id:
        return stripe.Customer.retrieve(stripe_customer_id)

    query = f"metadata['google']:'{email}'"
    customers = stripe.Customer.list(email=email) or \
                stripe.Customer.search(query=query)

    print("get_customer customers", list(map(lambda x: x['email'], customers)))
    if customers:
        return customers.data[0]
    else:
        return None


def is_active_subscriber(email: str) -> bool:
    stripe.api_key = get_api_key()

    customer = get_customer(email)
    print("is_active_subscriber customer", customer)
    if not customer:
        return False

    st.session_state.stripe_customer_id = customer["id"]
    st.session_state.stripe_customer_email = customer["email"]

    subscriptions = stripe.Subscription.list(customer=customer["id"])
    print("is_active_subscriber subscriptions", list(map(lambda x: x['status'], subscriptions)))

    subscriptions = list(filter(lambda x: x['status'] != "paused", subscriptions))
    st.session_state.subscriptions = subscriptions

    return len(subscriptions) > 0
