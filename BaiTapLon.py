from datetime import datetime

ten_file = "BTL/MenuFoods.txt"
menu_do_an = {}
ban_an = {}
doanh_thu = 0
doanh_thu_theo_ngay = {}
doanh_thu_theo_mon = {}
hoa_don = []


def doc_menu_tu_tap_tin(ten_file):
    menu = {}
    try:
        with open(ten_file, "r", encoding="utf-8") as tap:
            for line in tap:
                if line.strip():
                    parts = line.strip().split(",")
                    ID_mon = int(parts[0])
                    ten_mon = parts[1]
                    gia_tien = int(parts[2])
                    menu[ID_mon] = (ten_mon, gia_tien)
        return menu
    except FileNotFoundError:
        print(f"Tệp {ten_file} không tồn tại.")
        return {}
    except Exception as e:
        print(f"Lỗi khi đọc thực đơn: {e}")
        return {}


def ghi_menu_vao_tap_tin(menu, ten_file):
    try:
        with open(ten_file, "w", encoding="utf-8") as tap:
            for ID_mon, (ten_mon, gia_tien) in menu.items():
                tap.write(f"{ID_mon},{ten_mon},{gia_tien}\n")
        print("Thực đơn đã được cập nhật.")
    except Exception as e:
        print(f"Lỗi khi ghi thực đơn: {e}")


def hien_thi_thuc_don():
    if not menu_do_an:
        print("Thực đơn hiện tại trống.")
    else:
        print("\n=== Thực Đơn ===")
        for ID_mon, (ten_mon, gia_tien) in menu_do_an.items():
            print(f"{ID_mon}. {ten_mon} - {gia_tien} VND")


def xu_ly_dat_mon():
    if not menu_do_an:
        print("Thực đơn hiện tại trống. Vui lòng cập nhật thực đơn trước.")
        return

    so_ban = int(input("Nhập số bàn (1-20): "))
    if 1 <= so_ban <= 20:
        if so_ban not in ban_an:
            ban_an[so_ban] = {}

        print("\n=== Đặt Món ===")
        hien_thi_thuc_don()

        while True:
            ID_mon = int(input("\nNhập ID món: ( 0 để kết thúc ): "))
            if ID_mon == 0:
                print("\nKết thúc đặt món.")
                break

            if ID_mon in menu_do_an:
                so_luong = int(input(f"Nhập số lượng món {menu_do_an[ID_mon][0]}: "))
                if so_luong > 0:
                    if ID_mon in ban_an[so_ban]:
                        ban_an[so_ban][ID_mon] += so_luong
                    else:
                        ban_an[so_ban][ID_mon] = so_luong
                    print(
                        f"Đã thêm {so_luong} phần {menu_do_an[ID_mon][0]} vào bàn {so_ban}."
                    )
                else:
                    print("Số lượng không hợp lệ. Vui lòng thử lại.")
            else:
                print("Số món không hợp lệ. Vui lòng chọn lại.")

        print(f"\n=== Danh Sách Món Đã Đặt Bàn {so_ban} ===")
        if ban_an[so_ban]:
            for ID_mon, so_luong in ban_an[so_ban].items():
                ten_mon, gia_tien = menu_do_an[ID_mon]
                print(f"- {ten_mon}: {so_luong} phần")
        else:
            print("Chưa có món nào được đặt.")
    else:
        print("Số bàn không hợp lệ. Vui lòng nhập từ 1 đến 20.")


def xu_ly_thanh_toan():
    global doanh_thu

    danh_sach_ban = hien_thi_ban_chua_thanh_toan()
    if not danh_sach_ban:
        return

    try:
        so_ban = int(input("\nNhập số bàn cần thanh toán: "))
        if so_ban not in danh_sach_ban:
            print(f"Bàn {so_ban} không có món ăn hoặc không tồn tại.")
            return
    except ValueError:
        print("Vui lòng nhập số bàn hợp lệ.")
        return

    tong_tien = 0
    ngay_gio_hien_tai = datetime.now().strftime("%Y-%m-%d %H:%M")
    if ngay_gio_hien_tai.split(" ")[0] not in doanh_thu_theo_ngay:
        doanh_thu_theo_ngay[ngay_gio_hien_tai.split(" ")[0]] = 0

    print(f"\n=== Đơn Hàng Bàn {so_ban} ===")

    try:
        with open("BTL/DoanhThu.txt", "a", encoding="utf-8") as file:
            file.write(f"\n=== Hóa Đơn Bàn {so_ban} - Ngày {ngay_gio_hien_tai} ===\n")
            for ID_mon, so_luong in ban_an[so_ban].items():
                ten_mon, gia_tien = menu_do_an[ID_mon]
                thanh_tien = gia_tien * so_luong
                tong_tien += thanh_tien
                print(f"{ten_mon} - {so_luong} phần - {thanh_tien} VND")

                file.write(
                    f"Món: {ten_mon}, Số lượng: {so_luong}, Giá: {gia_tien} VND, Tổng: {thanh_tien} VND\n"
                )

            file.write(f"Tổng tiền: {tong_tien} VND\n")
            print(f"Tổng tiền: {tong_tien} VND")
    except Exception as e:
        print(f"Lỗi khi ghi hóa đơn: {e}")

    doanh_thu += tong_tien
    doanh_thu_theo_ngay[ngay_gio_hien_tai.split(" ")[0]] += tong_tien
    hoa_don.append(
        {"so_ban": so_ban, "tong_tien": tong_tien, "ngay": ngay_gio_hien_tai}
    )
    ban_an[so_ban].clear()
    print(f"Đã thanh toán thành công cho bàn {so_ban}.")

    
def hien_thi_ban_chua_thanh_toan():
    ban_chua_thanh_toan = [so_ban for so_ban, mon_an in ban_an.items() if mon_an]
    if not ban_chua_thanh_toan:
        print("\nKhông có bàn nào đang chờ thanh toán.")
        return []
    print("\n=== Danh Sách Bàn Chưa Thanh Toán ===")
    for so_ban in ban_chua_thanh_toan:
        print(f"- Bàn {so_ban}")
    return ban_chua_thanh_toan


def tong_ket_doanh_thu():
    print("\n=== Tổng Kết Doanh Thu ===")
    print("\nDanh sách các hóa đơn đã thanh toán:")
    for hoa_don_entry in hoa_don:
        print(
            f"Bàn {hoa_don_entry['so_ban']} - {hoa_don_entry['tong_tien']} VND - Ngày: {hoa_don_entry['ngay']}"
        )
    print(
        f"Doanh thu hôm nay: {doanh_thu_theo_ngay.get(datetime.now().strftime('%Y-%m-%d'), 0)} VND"
    )

    print("\n1. Sắp xếp theo thời gian (từ gần nhất đến lâu nhất)")
    print("2. Sắp xếp theo thời gian (từ lâu nhất đến gần nhất)")
    print("3. Sắp xếp theo giá thanh toán (từ lớn nhất đến bé nhất)")
    print("4. Sắp xếp theo giá thanh toán (từ bé nhất đến lớn nhất)")

    lua_chon_sap_xep = input("Nhập lựa chọn sắp xếp: ")
    if lua_chon_sap_xep == "1":
        hoa_don.sort(key=lambda x: x["ngay"], reverse=True)
    elif lua_chon_sap_xep == "2":
        hoa_don.sort(key=lambda x: x["ngay"])
    elif lua_chon_sap_xep == "3":
        hoa_don.sort(key=lambda x: x["tong_tien"], reverse=True)
    elif lua_chon_sap_xep == "4":
        hoa_don.sort(key=lambda x: x["tong_tien"])
    else:
        print("Lựa chọn không hợp lệ.")

    for hoa_don_entry in hoa_don:
        print(
            f"Bàn {hoa_don_entry['so_ban']} - {hoa_don_entry['tong_tien']} VND - Ngày: {hoa_don_entry['ngay']}"
        )


def quan_ly_thuc_don():
    while True:
        print("\n=== Quản Lý Thực Đơn ===")
        print("1. Thêm món mới")
        print("2. Sửa món")
        print("3. Xóa món")
        print("4. Hiển thị thực đơn")
        print("0. Quay lại")

        lua_chon = input("Nhập lựa chọn của bạn: ")

        if lua_chon == "1":
            them_mon()
        elif lua_chon == "2":
            sua_mon()
        elif lua_chon == "3":
            xoa_mon()
        elif lua_chon == "4":
            hien_thi_thuc_don()
        elif lua_chon == "0":
            break
        else:
            print("Lựa chọn không hợp lệ.")


def them_mon():
    try:
        ID_mon = int(input("Nhập số món (ví dụ: 1, 2, 3, ...): "))
        ten_mon = input("Nhập tên món: ")
        gia_tien = int(input("Nhập giá tiền của món (VND): "))

        if ID_mon in menu_do_an:
            print("Món này đã tồn tại trong thực đơn.")
        else:
            menu_do_an[ID_mon] = (ten_mon, gia_tien)
            ghi_menu_vao_tap_tin(menu_do_an, ten_file)
            print(f"Đã thêm món {ten_mon} vào thực đơn.")
    except ValueError:
        print("Dữ liệu nhập không hợp lệ. Vui lòng nhập lại.")


def sua_mon():
    try:
        ID_mon = int(input("Nhập số món cần sửa: "))
        if ID_mon not in menu_do_an:
            print("Món này không có trong thực đơn.")
        else:
            ten_mon = input("Nhập tên món mới: ")
            gia_tien = int(input("Nhập giá tiền mới của món (VND): "))
            menu_do_an[ID_mon] = (ten_mon, gia_tien)
            ghi_menu_vao_tap_tin(menu_do_an, ten_file)
            print(
                f"Đã cập nhật món {ID_mon} với tên mới: {ten_mon} và giá mới: {gia_tien} VND."
            )
    except ValueError:
        print("Dữ liệu nhập không hợp lệ. Vui lòng nhập lại.")


def xoa_mon():
    try:
        ID_mon = int(input("Nhập số món cần xóa: "))
        if ID_mon not in menu_do_an:
            print("Món này không có trong thực đơn.")
        else:
            del menu_do_an[ID_mon]
            ghi_menu_vao_tap_tin(menu_do_an, ten_file)
            print(f"Đã xóa món {ID_mon} khỏi thực đơn.")
    except ValueError:
        print("Dữ liệu nhập không hợp lệ. Vui lòng nhập lại.")


def xem_hoa_don():
    try:
        with open("BTL/DoanhThu.txt", "r", encoding="utf-8") as file:
            content = file.readlines()

            if not content:
                print("Không có hóa đơn nào được lưu trong tệp.")
                return

            print("\n=== Tất Cả Hóa Đơn ===")
            for line in content:
                print(line.strip())

    except FileNotFoundError:
        print("Tệp DoanhThu.txt không tồn tại.")
    except Exception as e:
        print(f"Lỗi khi đọc tệp: {e}")


def menu_chinh():
    while True:
        print(
            """
1. Đặt món
2. Thanh toán
3. Quản lý thực đơn
4. In danh sách món
5. Tổng kết doanh thu
6. Xem lại hóa đơn
0. Thoát
"""
        )

        lua_chon = input("Chọn thao tác: ")
        if lua_chon == "1":
            xu_ly_dat_mon()
        elif lua_chon == "2":
            xu_ly_thanh_toan()
        elif lua_chon == "3":
            quan_ly_thuc_don()
        elif lua_chon == "4":
            hien_thi_thuc_don()
        elif lua_chon == "5":
            tong_ket_doanh_thu()
        elif lua_chon == "6":
            xem_hoa_don()
        elif lua_chon == "0":
            break
        else:
            print("Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    menu_do_an = doc_menu_tu_tap_tin(ten_file)
    menu_chinh()
    ghi_menu_vao_tap_tin(menu_do_an, ten_file)
