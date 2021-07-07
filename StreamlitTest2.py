# new_app1.py
from MultiApp2 import MultiApp
import streamlit as st
def foo():
    st.title("Hello Foo")
def bar():
    st.title("Hello Bar")
    
app = MultiApp()
app.add_app("Foo", foo)
app.add_app("Bar", bar)
app.run()