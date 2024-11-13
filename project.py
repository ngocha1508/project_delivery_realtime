import streamlit as st
import pandas as pd
import random
import time

# Thiết lập tiêu đề ứng dụng
st.set_page_config(page_title="Ứng dụng Giao Hàng Theo Thời Gian Thực", layout="wide")
st.title("Ứng dụng Giao Hàng Theo Thời Gian Thực 🚚")

# Kiểm tra và khởi tạo dữ liệu đơn hàng trong session_state nếu chưa có
if 'orders' not in st.session_state:
    st.session_state.orders = []

# Hàm để thêm đơn hàng mới vào danh sách
def add_order(order_id, customer_name, address, status, estimated_delivery_time):
    new_order = {
        "order_id": order_id,
        "customer_name": customer_name,
        "address": address,
        "status": status,
        "estimated_delivery_time": estimated_delivery_time,
        "current_location": {
            "latitude": 10.762622 + random.uniform(-0.01, 0.01),
            "longitude": 106.660172 + random.uniform(-0.01, 0.01)
        }
    }
    st.session_state.orders.append(new_order)

# Hàm để hiển thị dữ liệu đơn hàng
def display_order_info(order):
    st.subheader(f"Đơn hàng #{order['order_id']}")
    st.write(f"**Khách hàng:** {order['customer_name']}")
    st.write(f"**Địa chỉ:** {order['address']}")
    st.write(f"**Trạng thái:** {order['status']}")
    st.write(f"**Dự kiến giao:** {order['estimated_delivery_time']}")

    # Hiển thị vị trí hiện tại
    if order['status'] == "Đang vận chuyển":
        st.map(pd.DataFrame([{
            "lat": order['current_location']['latitude'],
            "lon": order['current_location']['longitude']
        }], index=[0]))
    st.write("---")

# Sidebar để thêm đơn hàng mới
with st.sidebar:
    st.header("Nhập thông tin đơn hàng mới")
    order_id = st.text_input("Mã đơn hàng")
    customer_name = st.text_input("Tên khách hàng")
    address = st.text_input("Địa chỉ giao hàng")
    status = st.selectbox("Trạng thái", ["Chưa giao", "Đang vận chuyển", "Đã giao"])
    estimated_delivery_time = st.text_input("Thời gian dự kiến giao (hh:mm)")

    if st.button("Thêm đơn hàng"):
        if order_id and customer_name and address and estimated_delivery_time:
            add_order(order_id, customer_name, address, status, estimated_delivery_time)
            st.success(f"Đơn hàng #{order_id} đã được thêm.")
        else:
            st.error("Vui lòng nhập đầy đủ thông tin đơn hàng.")

# Thanh trượt để cài đặt thời gian làm mới
with st.sidebar:
    st.header("Cài đặt làm mới")
    refresh_rate = st.slider("Chọn thời gian làm mới (giây):", 5, 60, 10)
    st.write("Ứng dụng sẽ làm mới mỗi", refresh_rate, "giây.")

# Hiển thị danh sách đơn hàng
st.header("Danh sách đơn hàng đang vận chuyển")
st.text("Ứng dụng sẽ tự động làm mới để cập nhật trạng thái giao hàng.")

# Vòng lặp thời gian thực
while True:
    # Hiển thị từng đơn hàng trong danh sách
    for order in st.session_state.orders:
        display_order_info(order)

    # Dừng lại một khoảng thời gian trước khi tải lại
    time.sleep(refresh_rate)
    st.experimental_rerun()
