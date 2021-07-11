# 1. Library imports
from os import name
from numpy.core import numeric
import streamlit as st
import datetime
# import pandas as pd, numpy as np, 
import pickle
from streamlit.proto.NumberInput_pb2 import NumberInput


mRegressorModel=None


#De-serializing
def deserializeAndLoadModel():  
    global mRegressorModel   
    with open('random_forrest_regression_model.pkl','rb') as f:
        mRegressorModel=pickle.load(f)


# year=1&present_price=2&kms=3&fuel_type=cng&owner=dealer&transmission=manual

# present_price: float = Form(...), kms: float = Form(...),fuel_type: str = Form(...), seller: str = Form(...),transmission:str = Form(...), owner: str = Form(...)
def predict_output(yearOfPurchase,present_price,kms,fuelCheckedValue,sellerCheckedValue,transmissionCheckedValue,ownerCheckedValue):       

    Kms_Driven=kms
    Owner=[0 if(ownerCheckedValue=='First Owner') else 1 ]
    Seller_Type_Individual=[1 if(sellerCheckedValue=='Individual') else 0 ]
    Age=datetime.datetime.now().year-yearOfPurchase
    fuel=[1 if(i==fuelCheckedValue) else 0 for i in ['Diesel','Petrol']]  #[0 0] means fuel is of type CNG
    Transmission_Manual=[1 if(transmissionCheckedValue=='Manual') else 0 ]
    # Present_Price	Kms_Driven,Owner,Age,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual

    lst=[present_price,Kms_Driven]+Owner+[Age]+fuel+Seller_Type_Individual+Transmission_Manual
    # print(lst)
    predicted_val=mRegressorModel.predict([lst])[0]  #2d list
    # print(predicted_val)  #it's a list of length 1

    return predicted_val


def main():
    deserializeAndLoadModel()
    currentYear=datetime.datetime.now().year
    st.title("Car Price Prediction")
    html_code="""
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center">Streamlit Car Price Prediction ML App</h2>
    </div><br><br>
    """
    st.markdown(html_code,unsafe_allow_html=True)
    
    # yearOfPurchase=st.text_input("Year Of Purchase","eg: "+str(currentYear))
    yearOfPurchase=st.number_input("Year Of Purchase",currentYear)
    presentPrice=st.number_input("Present Price(in lakhs)",help="Price in lakhs",min_value=0.5,value=1.0)
    kmsDriven=st.number_input("KMS Driven",min_value=0.0,value=0.0)
    
    fuelTypes=["Petrol","Diesel","CNG"]
    fuelCheckedValue=st.radio("Fuel Type ",fuelTypes,index=0)  #setting the first option to be checked by default
    # st.write(fuelCheckedValue)
    # if(fuelCheckedValue=="CNG"):
    #     st.write("Great Choice")
    sellerTypes=["Individual","Dealer"]
    sellerCheckedValue=st.radio("Seller ",sellerTypes,index=0)  #setting the first option to be checked by default
    # st.write(sellerCheckedValue)
    transmissionTypes=["Manual","Automatic"]
    transmissionCheckedValue=st.radio("Transmission ",transmissionTypes,index=0)  #setting the first option to be checked by default
    # st.write(ownerCheckedValue)
    ownerTypes=["First Owner","Second Owner"]
    ownerCheckedValue=st.radio("Owner ",ownerTypes,index=0)  #setting the first option to be checked by default
    # st.write(ownerCheckedValue)

    if st.button("Calculate Selling Price"):
        # st.write([yearOfPurchase,presentPrice,kmsDriven,fuelCheckedValue,sellerCheckedValue,transmissionCheckedValue,ownerCheckedValue])
        predictedValueForSellingPrice=predict_output(yearOfPurchase,presentPrice,kmsDriven,fuelCheckedValue,sellerCheckedValue,transmissionCheckedValue,ownerCheckedValue)
        st.write(predictedValueForSellingPrice)

if __name__=="__main__":
    main()