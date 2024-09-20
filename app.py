import streamlit as st
import numpy as np
import pickle

model = pickle.load(open("C:/Users/sushm/PGA36/Projects/Capstone Project 2/new_trained_model.sav", 'rb'))

def encode_transaction_type(transaction_type):
    # Encoding 
    encoding = {
        "Payment": 0,
        "Transfer": 1,
        "Cash Out": 2,
        "Cash In": 3,
        "Debit": 4,
       
    }
    return encoding.get(transaction_type, -1)  # Returns -1 if type is not found

def online_payment(input_data):

    input_data_as_numpy_array = np.asarray(input_data, dtype=np.float64)
    
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    
    prediction = model.predict(input_data_reshaped)
    
    if prediction[0] == 0:
        return 'Not Fraud Transaction'
    else:
        return 'Fraud Transaction'

def main():
    st.title("Online Payment Fraud Detection")

    transaction_type = st.selectbox("Type of Transaction", options=["Payment", "Transfer", "Cash Out", "Cash In", "Debit"])

    amount = st.number_input("Amount", min_value=0.0, value=0.0, step=0.01)
    oldbalanceOrg = st.number_input("Old balance of Sender", min_value=0.0, value=0.0, step=0.01)
    oldbalanceDest = st.number_input("Old balance of Receiver", min_value=0.0, value=0.0, step=0.01)
    newbalanceDest = st.number_input("New Balance of Receiver", min_value=0.0, value=0.0, step=0.01)

    diagnosis = ''

    if st.button('Check Transaction'):
        encoded_type = encode_transaction_type(transaction_type)
        if encoded_type == -1:
            st.error("Invalid transaction type!")
        else:
            diagnosis = online_payment([encoded_type, amount, oldbalanceOrg, oldbalanceDest, newbalanceDest])
            st.success(diagnosis)

if __name__ == '__main__':
    main()
