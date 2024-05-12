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


def is_active_subscriber(email: str) -> bool:
    stripe.api_key = get_api_key()
    customers = stripe.Customer.list(email=email)
    print("is_active_subscriber customers", list(map(lambda x: x['email'], customers)))

    try:
        customer = customers.data[0]
    except IndexError:
        return False

    subscriptions = stripe.Subscription.list(customer=customer["id"])
    print("is_active_subscriber subscriptions", list(map(lambda x: x['status'], subscriptions)))

    subscriptions = list(filter(lambda x: x['status'] != "paused", subscriptions))
    st.session_state.subscriptions = subscriptions

    return len(subscriptions) > 0
