import json
import os
import time
import streamlit as st
from arikedb import Arikedb


arikedb = st.session_state.get("arikedb", None)

if not isinstance(arikedb, Arikedb):
    st.title("No connection")
else:
    st.title("Collections")
    st.markdown(f"#### Connected to '{st.session_state.connected_server}' ({arikedb._host}:{arikedb._port})")

    collections = arikedb.collections()

    with st.expander("New Collection"):
        name = st.text_input("Collection Name", placeholder="MyCollection")

        if st.button("Create"):
            response = arikedb.create_collections([name])
            exists = response.get("already_exists", [])
            lic_exceeded = response.get("license_exceeded", [])

            if len(exists) > 0:
                st.error(f"Collection {name} already exists!")
            elif len(lic_exceeded) > 0:
                st.error("License limit exceeded!")
            else:
                st.success(f"Collection {name} created successfully!")
                time.sleep(0.5)
                st.rerun()

    name, actions = st.columns(2)

    name.markdown("### Name")
    actions.markdown("### Actions")

    for collection in collections:
        name.write(collection.name)
        b1, b2 = actions.columns(2)
        if b1.button("Delete", key=f"delete-{collection.name}"):
            arikedb.delete_collections([collection.name])
            st.rerun()
        if b2.button("Use", key=f"use-{collection.name}"):
            st.session_state.collection = collection
            st.switch_page("pages/3_Data.py")
