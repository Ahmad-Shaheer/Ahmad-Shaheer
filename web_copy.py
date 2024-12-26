import streamlit as st 
import functions 
FILEPATH = 'todos.txt'

todos = functions.read_todos(FILEPATH)
def add_todo():
    todo = st.session_state['todos']  + '\n'
    todos.append(todo)
    functions.write_todos(FILEPATH, todos)
    

# st.session_state['check']

st.title('Todo App')
st.header('this is my todo app')

todos = functions.read_todos(FILEPATH)
for index, todo in enumerate(todos):
    checkbox = st.checkbox(todo,key = todo ) # dynamic key so it is different for every created checkbox
    if checkbox:
        todos.pop(index)
        functions.write_todos(FILEPATH, todos) # this is to update the text file on the backend
        st.rerun()                             # no sure what rerun does. I think it runs the code a second time
        
st.text_input(label = '',placeholder = 'Add a todo...', on_change = add_todo ,key = 'todos')

'''
core concepts: 
since the session state is a dictionary class type, it nees to take the \
key value as the key of a dictionary to access the relevant value. for this reason it is enclosed in square brackes as opposed to the conventional paranthesis that we usually see in methods.
'''