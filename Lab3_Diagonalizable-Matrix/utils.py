def find_eigenvalues(poly):
    """Tìm các trị riêng từ đa thức đặc trưng (chỉ xét nghiệm thực)"""
    # Đa thức đặc trưng có các hệ số theo lũy thừa giảm dần
    print("Đa thức đặc trưng có các hệ số:", poly)
    
    # Loại bỏ hệ số 0 ở đầu đa thức
    while len(poly) > 0 and abs(poly[0]) < 1e-10:
        poly = poly[1:]
    
    # Nếu đa thức rỗng hoặc hằng số, không có nghiệm
    if len(poly) <= 1:
        return {}
    
    # Chuẩn hóa đa thức để hệ số cao nhất là 1
    poly = [coef / poly[0] for coef in poly]
    
    # Tìm nghiệm của đa thức bằng phương pháp cải tiến
    roots_with_multiplicity = find_polynomial_roots_with_multiplicity(poly)
    
    # Làm tròn nghiệm để tránh sai số số học
    eigenvalues = {}
    for root, multiplicity in roots_with_multiplicity:
        # Làm tròn số thực để tránh sai số
        if abs(root - round(root)) < 1e-10:
            root = round(root)
        eigenvalues[root] = multiplicity
    
    print("Trị riêng và bội số tương ứng:", eigenvalues)
    return eigenvalues

def find_polynomial_roots_with_multiplicity(poly, tol=1e-10):
    """Tìm nghiệm thực của đa thức kèm theo bội số"""
    n = len(poly) - 1  # Bậc của đa thức
    
    # Với đa thức bậc 1: ax + b = 0
    if n == 1:
        root = -poly[1] / poly[0]
        return [(root, 1)]
    
    # Với đa thức bậc 2: ax^2 + bx + c = 0, dùng công thức nghiệm
    elif n == 2:
        a, b, c = poly
        delta = b**2 - 4*a*c
        
        if abs(delta) < 1e-10:  # Delta gần 0 - nghiệm kép
            root = -b / (2*a)
            return [(root, 2)]
        elif delta > 0:
            sqrt_delta = delta**0.5
            root1 = (-b + sqrt_delta) / (2*a)
            root2 = (-b - sqrt_delta) / (2*a)
            return [(root1, 1), (root2, 1)]
        else:
            # Đa thức có nghiệm phức, nhưng ta chỉ quan tâm đến nghiệm thực
            return []
    
    # Với đa thức bậc 3 trở lên, sử dụng phương pháp tìm nghiệm và xác định bội
    else:
        roots_with_multiplicity = []
        working_poly = poly.copy()
        
        while len(working_poly) > 1:  # Đa thức có bậc ít nhất là 1
            # Tìm một nghiệm
            roots = find_real_roots_with_bisection(working_poly)
            if not roots:
                break  # Không tìm thấy nghiệm thực nào khác
            
            root = roots[0]  # Lấy một nghiệm đã tìm được
            
            # Xác định bội của nghiệm bằng cách kiểm tra đạo hàm
            multiplicity = 0
            current_poly = working_poly.copy()
            
            while len(current_poly) > 1:
                # Kiểm tra nếu root là nghiệm của đa thức hiện tại
                value = evaluate_polynomial(current_poly, root)
                if abs(value) > tol:
                    break
                
                multiplicity += 1
                current_poly = derivative_polynomial(current_poly)
            
            # Thêm nghiệm và bội số vào kết quả
            roots_with_multiplicity.append((root, multiplicity))
            
            # Giảm bậc đa thức bằng cách chia cho (x - root)^multiplicity
            for _ in range(multiplicity):
                working_poly = polynomial_deflation(working_poly, root)
        
        return roots_with_multiplicity

def polynomial_deflation(poly, root):
    """Chia đa thức cho (x - root) bằng thuật toán Horner"""
    n = len(poly)
    if n <= 1:
        return []
    
    result = [poly[0]]
    for i in range(1, n - 1):
        result.append(poly[i] + result[i-1] * root)
    
    # Kiểm tra phần dư (remainder) gần 0
    remainder = poly[n-1] + result[n-2] * root
    if abs(remainder) > 1e-8:
        print(f"Cảnh báo: Phần dư khi chia đa thức cho (x - {root}) không gần 0: {remainder}")
    
    return result

# def find_polynomial_roots(poly):
#     """Tìm nghiệm thực của đa thức"""
#     n = len(poly) - 1  # Bậc của đa thức
    
#     # Với đa thức bậc 1: ax + b = 0
#     if n == 1:
#         return [-poly[1] / poly[0]]
    
#     # Với đa thức bậc 2: ax^2 + bx + c = 0, dùng công thức nghiệm
#     elif n == 2:
#         a, b, c = poly
#         delta = b**2 - 4*a*c
        
#         if abs(delta) < 1e-10:  # Delta gần 0
#             return [-b / (2*a), -b / (2*a)]
#         elif delta > 0:
#             sqrt_delta = delta**0.5
#             return [(-b + sqrt_delta) / (2*a), (-b - sqrt_delta) / (2*a)]
#         else:
#             # Đa thức có nghiệm phức, nhưng ta chỉ quan tâm đến nghiệm thực
#             return []
    
#     # Với đa thức bậc 3 trở lên, sử dụng phương pháp lặp
#     else:
#         return find_real_roots_with_bisection(poly)

def evaluate_polynomial(poly, x):
    """Tính giá trị của đa thức tại x"""
    result = 0
    for coef in poly:
        result = result * x + coef
    return result

def find_real_roots_with_bisection(poly, range_min=-100, range_max=100, steps=1000, tol=1e-10):
    """Tìm nghiệm thực của đa thức bằng phương pháp chia đôi"""
    roots = []
    step_size = (range_max - range_min) / steps
    
    # Tìm các khoảng có thể chứa nghiệm
    x_prev = range_min
    y_prev = evaluate_polynomial(poly, x_prev)
    
    for i in range(1, steps + 1):
        x_curr = range_min + i * step_size
        y_curr = evaluate_polynomial(poly, x_curr)
        
        # Kiểm tra xem có đổi dấu hay không
        if y_prev * y_curr <= 0:
            # Tìm nghiệm chính xác hơn bằng phương pháp chia đôi
            root = bisection_method(poly, x_prev, x_curr, tol)
            # Kiểm tra xem nghiệm này đã có trong danh sách chưa
            is_duplicate = False
            for existing_root in roots:
                if abs(root - existing_root) < tol:
                    is_duplicate = True
                    break
            if not is_duplicate:
                roots.append(root)
        
        x_prev = x_curr
        y_prev = y_curr
    
    # Tìm nghiệm dùng phương pháp Newton để tăng độ chính xác
    refined_roots = []
    for root in roots:
        refined_root = newton_method(poly, root, tol)
        # Kiểm tra xem nghiệm tinh chỉnh đã có trong danh sách chưa
        is_duplicate = False
        for existing_root in refined_roots:
            if abs(refined_root - existing_root) < tol:
                is_duplicate = True
                break
        if not is_duplicate:
            refined_roots.append(refined_root)
    
    return refined_roots

def bisection_method(poly, a, b, tol=1e-10, max_iter=100):
    """Tìm nghiệm của đa thức trong khoảng [a, b] bằng phương pháp chia đôi"""
    fa = evaluate_polynomial(poly, a)
    fb = evaluate_polynomial(poly, b)
    
    # Kiểm tra xem khoảng có chứa nghiệm không
    if fa * fb > 0:
        # Không có nghiệm trong khoảng hoặc có số chẵn nghiệm
        return (a + b) / 2
    
    # Nếu một trong hai đầu mút là nghiệm
    if abs(fa) < tol:
        return a
    if abs(fb) < tol:
        return b
    
    # Thực hiện phương pháp chia đôi
    for _ in range(max_iter):
        c = (a + b) / 2
        fc = evaluate_polynomial(poly, c)
        
        if abs(fc) < tol:
            return c
        
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
        
        # Điều kiện dừng
        if (b - a) < tol:
            return (a + b) / 2
    
    return (a + b) / 2

def newton_method(poly, x0, tol=1e-10, max_iter=100):
    """Tìm nghiệm của đa thức bằng phương pháp Newton"""
    x = x0
    
    for _ in range(max_iter):
        # Tính giá trị của đa thức và đạo hàm tại x
        f_x = evaluate_polynomial(poly, x)
        
        if abs(f_x) < tol:
            return x
        
        # Tính đạo hàm
        df_x = 0
        for i in range(len(poly) - 1):
            df_x = df_x * x + (len(poly) - i - 1) * poly[i]
        
        if abs(df_x) < tol:  # Tránh chia cho 0
            break
        
        # Áp dụng công thức Newton
        x_new = x - f_x / df_x
        
        # Kiểm tra hội tụ
        if abs(x_new - x) < tol:
            return x_new
        
        x = x_new
    
    return x

def derivative_polynomial(poly):
    """Tính đạo hàm của đa thức"""
    n = len(poly)
    if n <= 1:
        return [0]
    
    deriv = []
    for i in range(n - 1):
        deriv.append((n - i - 1) * poly[i])
    
    return deriv

def find_real_roots_with_newton(poly, initial_guesses=None, tol=1e-10):
    """Tìm nghiệm thực của đa thức bằng phương pháp Newton với nhiều giá trị ban đầu"""
    if initial_guesses is None:
        # Tạo các giá trị ban đầu trong khoảng [-10, 10]
        initial_guesses = [-10 + i for i in range(21)]
    
    roots = []
    
    for guess in initial_guesses:
        root = newton_method(poly, guess, tol)
        
        # Kiểm tra xem đây có phải là nghiệm thực không
        f_root = evaluate_polynomial(poly, root)
        if abs(f_root) < tol:
            # Kiểm tra xem nghiệm này đã có trong danh sách chưa
            is_duplicate = False
            for existing_root in roots:
                if abs(root - existing_root) < tol:
                    is_duplicate = True
                    break
            if not is_duplicate:
                roots.append(root)
    
    return roots