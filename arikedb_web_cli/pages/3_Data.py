import json
import os
import time
import streamlit as st
from arikedb import Arikedb, Collection, TsVariable, Stack, Fifo, SortedList, ValueType


arikedb = st.session_state.get("arikedb", None)

if not isinstance(arikedb, Arikedb):
    st.title("No connection")
else:
    st.title("Data")
    st.markdown(f"#### Connected to '{st.session_state.connected_server}' ({arikedb._host}:{arikedb._port})")
    collection = st.session_state.get("collection", None)

    if not isinstance(collection, Collection):
        st.markdown("## No collection selected")
    else:
        st.markdown(f"## Collection: '{collection.name}'")
        with st.expander("New Variable"):
            name = st.text_input("Collection Name", placeholder="x1")
            vtype = ValueType(st.selectbox(
                "Type",
                [v.value for v in ValueType],
                format_func=lambda v: ValueType(v).name
            ))

            var_type = st.selectbox(
                "Variable Type",
                ["Time Series", "Stack", "Fifo", "Sorted List"]
            )
            if var_type in ["Stack", "Fifo", "Sorted List"]:
                length = st.number_input("Length", min_value=1, value=10)

            if st.button("Create"):
                if var_type == "Time Series":
                    response = collection.create_ts_variables([(name, vtype)])
                elif var_type == "Stack":
                    response = collection.create_stacks([(name, vtype, length)])
                elif var_type == "Fifo":
                    response = collection.create_fifos([(name, vtype, length)])
                elif var_type == "Sorted List":
                    response = collection.create_sorted_lists([(name, vtype, length)])
                else:
                    st.error("Invalid variable type")
                    response = {}

                already_exists = response.get("already_exists", [])
                if len(already_exists) > 0:
                    st.error(f"Variable {name} already exists!")
                else:
                    st.success(f"Variable {name} created successfully!")
                time.sleep(0.5)
                st.rerun()

        ts_vars = collection.ts_variables()
        stacks = collection.stacks()
        fifos = collection.fifos()
        sorted_lists = collection.sorted_lists()

        variables = []
        for ts_var in ts_vars:
            variables.append({
                "name": ts_var.name,
                "type": f"Time Series: {ts_var.vtype.name}",
                "type_": 0
            })

        for stack in stacks:
            variables.append({
                "name": stack.name,
                "type": f"Stack: {stack.vtype.name}",
                "type_": 1
            })

        for fifo in fifos:
            variables.append({
                "name": fifo.name,
                "type": f"Fifo: {fifo.vtype.name}",
                "type_": 2
            })

        for sorted_list in sorted_lists:
            variables.append({
                "name": sorted_list.name,
                "type": f"Sorted List: {sorted_list.vtype.name}",
                "type_": 3
            })

        name, vtype, actions = st.columns(3)

        name.markdown("### Name")
        vtype.markdown("### Type")
        actions.markdown("### Actions")

        for variable in variables:
            name.write(variable["name"])
            vtype.write(variable["type"])

            if actions.button("Delete", key=f"delete-{variable['name']}"):
                if variable["type_"] == 0:
                    collection.delete_ts_variables([variable["name"]])
                elif variable["type_"] == 1:
                    collection.delete_stacks([variable["name"]])
                elif variable["type_"] == 2:
                    collection.delete_fifos([variable["name"]])
                elif variable["type_"] == 3:
                    collection.delete_sorted_lists([variable["name"]])
                st.rerun()
