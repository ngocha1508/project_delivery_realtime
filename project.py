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

# Kiểm tra và khởi tạo tuyến đường mẫu cho các đơn hàng
if 'routes' not in st.session_state:
    st.session_state.routes = {}

# Hàm để thêm đơn hàng mới vào danh sách và tạo tuyến đường mẫu
def add_order(order_id, customer_name, address, status, estimated_delivery_time):
    # Tạo vị trí giả lập cho điểm bắt đầu và điểm kết thúc
    start_location = {"latitude": 10.762622, "longitude": 106.660172}
    end_location = {"latitude": start_location["latitude"] + random.uniform(0.01, 0.05),
                    "longitude": start_location["longitude"] + random.uniform(0.01, 0.05)}

    # Lưu tuyến đường mẫu (danh sách các điểm từ start đến end)
    route = [start_location]
    for i in range(10):  # Giả lập 10 điểm trên tuyến đường
        lat_step = (end_location["latitude"] - start_location["latitude"]) / 10
        lon_step = (end_location["longitude"] - start_location["longitude"]) / 10
        route.append({
            "latitude": start_location["latitude"] + lat_step * (i + 1),
            "longitude": start_location["longitude"] + lon_step * (i + 1)
        })
    st.session_state.routes[order_id] = route

    # Thêm đơn hàng mới vào danh sách
    new_order = {
        "order_id": order_id,
        "customer_name": customer_name,
        "address": address,
        "status": status,
        "estimated_delivery_time": estimated_delivery_time,
        "current_position_index": 0  # Chỉ mục hiện tại của vị trí trên tuyến đường
    }
    st.session_state.orders.append(new_order)

# Hàm để cập nhật vị trí của các đơn hàng đang vận chuyển
def update_order_location():
    for order in st.session_state.orders:
        if order["status"] == "Đang vận chuyển":
            # Cập nhật vị trí của đơn hàng trên tuyến đường
            if order["current_position_index"] < len(st.session_state.routes[order["order_id"]]) - 1:
                order["current_position_index"] += 1  # Di chuyển đến điểm tiếp theo trên tuyến đường
            else:
                order["status"] = "Đã giao"  # Nếu đã đến điểm cuối thì cập nhật trạng thái thành "Đã giao"

# Hàm để hiển thị dữ liệu đơn hàng và biểu đồ tuyến đường
def display_order_info(order):
    st.subheader(f"Đơn hàng #{order['order_id']}")
    st.write(f"**Khách hàng:** {order['customer_name']}")
    st.write(f"**Địa chỉ:** {order['address']}")
    st.write(f"**Trạng thái:** {order['status']}")
    st.write(f"**Dự kiến giao:** {order['estimated_delivery_time']}")

    # Hiển thị tuyến đường từ điểm bắt đầu đến vị trí hiện tại
    route = st.session_state.routes[order["order_id"]]
    current_position_index = order["current_position_index"]
    
    if order['status'] == "Đang vận chuyển":
        # Hiển thị bản đồ với quãng đường từ đầu đến vị trí hiện tại
        route_df = pd.DataFrame(route[:current_position_index + 1])  # Dữ liệu tuyến đường từ đầu đến vị trí hiện tại
        st.map(route_df)

        # Hiển thị biểu đồ tuyến đường để theo dõi tiến trình giao hàng
        st.line_chart(route_df, x="longitude", y="latitude")

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
# Cập nhật vị trí đơn hàng và hiển thị danh sách đơn hàng
while True:
    # Cập nhật vị trí của các đơn hàng
    update_order_location()

    # Hiển thị từng đơn hàng trong danh sách
    for order in st.session_state.orders:
        display_order_info(order)

    # Dừng lại một khoảng thời gian trước khi tải lại
    time.sleep(refresh_rate)
    st.experimental_rerun()
