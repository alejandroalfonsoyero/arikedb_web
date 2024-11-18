import json
import os
import time
import streamlit as st
from arikedb import Arikedb


def connect_to_db(host, port, username, password, alias):
    try:
        st.session_state.arikedb = Arikedb(host, port, username, password).connect()
        st.success("Successfully connected to the database.")
        time.sleep(0.5)
        st.session_state.connected_server = alias
        st.switch_page("pages/2_Collections.py")
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")


def load_connections():
    if os.path.isfile("current_connections.json"):
        with open("current_connections.json", "r") as f:
            return json.load(f)
    else:
        return {}


def save_connections(connections):
    with open("current_connections.json", "w") as f:
        json.dump(connections, f, separators=(",", ":"))


connections = load_connections()
st.title("Connection")

with st.expander("New Connection"):
    alias = st.text_input("Alias", placeholder="Connection Alias")
    host = st.text_input("Host", value="127.0.0.1")
    port = st.number_input("Port", min_value=1, max_value=65535, value=6923)
    use_credentials = st.checkbox("Use Credentials")
    if use_credentials:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
    else:
        username = None
        password = None
    if st.button("Save"):
        id = 0
        for conn_id, connection in connections.items():
            conn_id = int(conn_id)
            if conn_id > id:
                id = conn_id
        id += 1
        connections[id] = {
            "alias": alias,
            "host": host,
            "port": port,
            "use_credentials": use_credentials,
            "username": username,
            "password": password
        }
        save_connections(connections)
        st.rerun()

alias, url, actions = st.columns(3)

alias.markdown("### Alias")
url.markdown("### URL")
actions.markdown("### Actions")

for conn_id, connection in connections.items():
    alias.write(connection["alias"])
    url.write(f"{connection['host']}:{connection['port']}")
    b1, b2 = actions.columns(2)
    if b1.button("Delete", key=f"delete-{conn_id}"):
        del connections[conn_id]
        save_connections(connections)
        st.rerun()
    if b2.button("Connect", key=f"connect-{conn_id}"):
        connect_to_db(connection["host"], int(connection["port"]),
                      connection["username"], connection["password"],
                      connection["alias"])
