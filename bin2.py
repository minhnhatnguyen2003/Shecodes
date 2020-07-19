import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import geocoder 
import matplotlib.pyplot as plt
from math import cos, asin, sqrt
from geopy.geocoders import Nominatim
#######Phần 1
st.title('Bài đăng')
st.header('Bạn muốn bán đồng nát gồm những gì ?')
if st.checkbox('Giấy'):
	t1 = 'Giấy'
if st.checkbox('Đồ điện tử cũ'):
	t2 = 'Đồ điện tử cũ'
if st.checkbox('Nhựa'):
	t3 = 'Nhựa'
t4 = st.text_input('Khác')
t5 = [t1,t2,t3,t4]
#####load ảnh
image = Image.open(st.file_uploader("Ảnh chụp đồng nát", type=("png", "jpg")))

####Phần 2
st.header('Chọn địa điểm')
data = pd.read_csv (r'C:/Users/ACER/Documents/shecodes/HCM - Sheet1 (1).csv')  
df = pd.DataFrame(data, columns= ['dis','lat','lon','city','add','name_dvtc','sdt'])
### default: địa chỉ hiện tại; nếu chọn khu vực, địa chỉ hiện tại = False
if st.checkbox('Sử dụng địa chỉ hiện tại'):
	g = geocoder.ip('me')
	lat_ad=g.latlng[0]
	lon_ad=g.latlng[1]
	def distance(lat1, lon1, lat2, lon2):
		p = 0.017453292519943295
		a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
		return 12742 * asin(sqrt(a))
	def closest(data,v):
		return min(data, key=lambda p: distance(v['lat'],v['lon'],p['lat'],p['lon']))
	v = {'lat':float(lat_ad), 'lon':float(lon_ad)}
	check_des = v
	tmp = [{'lat': df['lat'][i], 'lon': df['lon'][i]} for i in range(len(df))]
	df_end = df[(df.lat == (closest(tmp, v)['lat'])) & (df.lon == closest(tmp, v)['lon'])]
	address = g.city
	check_des = address


else :
  city_now = st.selectbox('Bạn đang ở', df.city.unique())
  dis_now = st.selectbox('Bạn đang ở quận', df.dis.unique())
  df_end = df[(df.city == city_now) & (df.dis == dis_now)]
  check_des = [df_end.city, df_end.dis]

###################đợi 
if st.button('Đăng'):
        with st.spinner("Đang đăng"):
        	st.write('Đăng thành công')
        	data_post = {
        	"Đồng nát" : [t5],
        	"Địa điểm" : [check_des]
        	}
        	df_post = pd.DataFrame(data_post)
        	df_post
        	st.image(image, caption='Ảnh', use_column_width=True)
        	st.write('Những người thu mua đồng nát tiềm năng', df_end)
        	st.map(df_end)
#st.write('yy')
