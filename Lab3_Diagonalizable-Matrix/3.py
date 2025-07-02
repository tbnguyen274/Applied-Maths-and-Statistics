def create_matrix(rows, cols, default_value=0):
    """Tạo ma trận với rows hàng và cols cột"""
    return [[default_value for _ in range(cols)] for _ in range(rows)]

def create_identity_matrix(n):
    """Tạo ma trận đơn vị kích thước n x n"""
    identity = create_matrix(n, n)
    for i in range(n):
        identity[i][i] = 1
    return identity

def matrix_copy(A):
    """Tạo bản sao của ma trận A"""
    return [row[:] for row in A]

def matrix_multiply(A, B):
    """Nhân hai ma trận A và B"""
    m = len(A)
    n = len(A[0])
    p = len(B[0])
    C = create_matrix(m, p)
    
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    
    return C

def matrix_subtract(A, B):
    """Trừ hai ma trận A và B"""
    m = len(A)
    n = len(A[0])
    C = create_matrix(m, n)
    
    for i in range(m):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
    
    return C

def scalar_multiply(scalar, A):
    """Nhân ma trận A với một số scalar"""
    m = len(A)
    n = len(A[0])
    C = create_matrix(m, n)
    
    for i in range(m):
        for j in range(n):
            C[i][j] = scalar * A[i][j]
    
    return C

def matrix_subtract_lambda_I(A, lambda_val):
    """Tạo ma trận A - lambda*I"""
    n = len(A)
    result = matrix_copy(A)
    
    for i in range(n):
        result[i][i] -= lambda_val
    
    return result

def polynomial_multiply(p1, p2):
    """Nhân hai đa thức p1 và p2"""
    deg1 = len(p1) - 1
    deg2 = len(p2) - 1
    result = [0] * (deg1 + deg2 + 1)
    
    for i in range(len(p1)):
        for j in range(len(p2)):
            result[i + j] += p1[i] * p2[j]
    
    return result

def determinant(A):
    """Tính định thức của ma trận A bằng phương pháp khai triển theo cột"""
    n = len(A)
    
    # Trường hợp cơ bản
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    
    det = 0
    for j in range(n):
        # Tạo ma trận con bằng cách loại bỏ hàng 0 và cột j
        minor = create_matrix(n-1, n-1)
        for i in range(1, n):
            minor_col = 0
            for k in range(n):
                if k != j:
                    minor[i-1][minor_col] = A[i][k]
                    minor_col += 1
        
        cofactor = A[0][j] * determinant(minor) * ((-1) ** j)
        det += cofactor
    
    return det

def characteristic_polynomial(A):
    """Tính đa thức đặc trưng P(λ) = det(A - λI) theo thứ tự lũy thừa giảm dần"""
    n = len(A)
    
    # Với n = 1, P(λ) = λ - a
    if n == 1:
        return [1, -A[0][0]]  # [λ, c]
    
    # Với n = 2, P(λ) = λ² - trace(A)λ + det(A)
    if n == 2:
        trace = A[0][0] + A[1][1]
        det_A = A[0][0] * A[1][1] - A[0][1] * A[1][0]
        return [1, -trace, det_A]  # [λ², λ, c]
    
    # Với n = 3, tính trực tiếp
    if n == 3:
        a, b, c = A[0][0], A[0][1], A[0][2]
        d, e, f = A[1][0], A[1][1], A[1][2]
        g, h, i = A[2][0], A[2][1], A[2][2]
        
        # P(λ) = λ³ - trace(A)λ² + (các minor 2x2)λ - det(A)
        trace = a + e + i
        
        # Tổng các định thức minor 2x2 chính
        minor_sum = (a*e + a*i + e*i) - (b*d + c*g + f*h)
        
        # Định thức của A
        det_A = a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)
        
        return [-1, trace, -minor_sum, det_A]  # [λ³, λ², λ, c₀]
    
    # Với n > 3, quay lại dùng phương pháp khai triển
    coeffs = [0] * (n + 1)
    coeffs[0] = (-1)**n  # Hệ số của λⁿ
    
    for k in range(1, n+1):
        # Tính (-1)ⁿ⁻ᵏ * định thức của minor kích thước (n-k)
        sign = (-1)**(n-k)
        
        # Lấy tất cả các minor có kích thước n-k
        sum_det = 0
        # Trường hợp đơn giản: k = n -> toàn bộ ma trận
        if k == n:
            sum_det = determinant(A)
        # Trường hợp k = 1: tính tổng các phần tử đường chéo (trace)
        elif k == 1:
            sum_det = sum(A[i][i] for i in range(n))
        # Trường hợp k = 0: hệ số của λⁿ là (-1)ⁿ
        elif k == 0:
            sum_det = 1
        else:
            # Trường hợp phức tạp hơn: cần phải xem xét tất cả các minor
            # Để đơn giản hóa, ta có thể dùng thư viện numpy
            import numpy as np
            np_A = np.array(A)
            if k == 2:  # Trường hợp k = 2 (tương ứng với n-2)
                sum_det = 0
                for i in range(n):
                    for j in range(i+1, n):
                        # Tạo minor bằng cách loại bỏ hàng i, j và cột i, j
                        minor = get_minor_matrix(A, [i, j], [i, j])
                        sum_det += determinant(minor)
            
        coeffs[k] = sign * sum_det
        
    return coeffs

def get_minor_matrix(matrix, rows_to_remove, cols_to_remove):
    """Trả về ma trận con khi loại bỏ các hàng và cột chỉ định"""
    n = len(matrix)
    minor = []
    
    for i in range(n):
        if i not in rows_to_remove:
            row = []
            for j in range(n):
                if j not in cols_to_remove:
                    row.append(matrix[i][j])
            minor.append(row)
    
    return minor

# def characteristic_polynomial(A):
#     """Tính đa thức đặc trưng det(A-λI) sử dụng numpy"""
#     import numpy as np
    
#     n = len(A)
#     np_A = np.array(A)
    
#     # Tính đa thức đặc trưng
#     # np.poly tính đa thức từ các nghiệm, nên cần các giá trị riêng
#     eigenvalues = np.linalg.eigvals(np_A)
    
#     # Tính đa thức từ nghiệm
#     poly = np.poly(eigenvalues)
    
#     # Chuyển về dạng list với độ chính xác cao hơn
#     return poly.tolist()


def find_eigenvalues(poly):
    """Tìm các trị riêng từ đa thức đặc trưng"""
    # Đa thức đặc trưng có các hệ số theo lũy thừa giảm dần
    print("Đa thức đặc trưng có các hệ số:", poly)
    
    # Tìm nghiệm của đa thức
    import numpy as np
    roots = np.roots(poly)
    # đổi về list để dễ thao tác
    roots = roots.tolist()

    # Làm tròn nghiệm để tránh sai số số học
    # nếu |số - phần nguyên| < thì chỉ lấy phần nguyên
    for i in range(len(roots)):
        if abs(roots[i] - roots[i]) < 1e-10:
            roots[i] = round(roots[i])
    
    print("Các nghiệm của đa thức đặc trưng:", roots)
    
    # Đếm bội của mỗi trị riêng
    eigenvalues = {}
    for root in roots:
        eigenvalues[root] = eigenvalues.get(root, 0) + 1
    
    print("Trị riêng và bội số tương ứng:", eigenvalues)
    return eigenvalues


def gauss_elimination(A):
    """Đưa ma trận A về dạng bậc thang rút gọn (RREF)"""
    A = [row[:] for row in A]  # Copy ma trận
    m = len(A)
    n = len(A[0])
    
    h = 0  # Chỉ số hàng pivot hiện tại
    k = 0  # Chỉ số cột pivot hiện tại
    pivot_positions = []  # Lưu vị trí các pivot
    
    while h < m and k < n:
        # Tìm pivot trong cột k
        max_val = 0
        max_row = h
        for i in range(h, m):
            if abs(A[i][k]) > max_val:
                max_val = abs(A[i][k])
                max_row = i
        
        if abs(A[max_row][k]) < 1e-10:  # Gần như bằng 0
            # Không có pivot trong cột này
            k += 1
            continue
        
        # Hoán đổi hàng
        if max_row != h:
            A[h], A[max_row] = A[max_row], A[h]
        
        # Lưu vị trí pivot
        pivot_positions.append(k)
        
        # Chuẩn hóa hàng pivot để biến phần tử pivot thành 1
        pivot = A[h][k]
        for j in range(k, n):
            A[h][j] /= pivot
        
        # Khử tất cả các hàng khác (cả trên và dưới) để cột pivot chỉ có 1 phần tử khác 0
        for i in range(m):
            if i != h:
                factor = A[i][k]
                for j in range(k, n):
                    A[i][j] -= factor * A[h][j]
        
        h += 1
        k += 1
    
    # Làm sạch số nhỏ thành 0
    for i in range(m):
        for j in range(n):
            if abs(A[i][j]) < 1e-10:
                A[i][j] = 0.0
    
    return A, pivot_positions

def find_eigenvectors(A, eigenval, multiplicity):
    """Tìm vector riêng tương ứng với trị riêng eigenval"""
    n = len(A)
    A_lambda = matrix_subtract_lambda_I(A, eigenval)
    
    # Đưa A_lambda về dạng bậc thang
    rref_matrix, pivot_positions = gauss_elimination(A_lambda)
    
    # Tìm các biến tự do
    free_vars = [j for j in range(n) if j not in pivot_positions]
    
    # Số chiều không gian nghiệm
    dim = len(free_vars)
    
    print(f"Trị riêng {eigenval} có bội {multiplicity} và không gian nghiệm có số chiều {dim}")
    
    if dim < multiplicity:
        return None  # Ma trận không chéo hóa được
    
    # Tìm cơ sở của không gian nghiệm
    basis = []
    
    for free_var in free_vars:
        # Tạo vector với biến tự do được gán giá trị 1
        vec = [0] * n
        vec[free_var] = 1.0
        
        # Thay thế ngược từ dưới lên để tìm các giá trị còn lại
        for i in range(len(pivot_positions) - 1, -1, -1):
            row = i
            col = pivot_positions[i]
            
            # Tính tổng các thành phần đã biết
            sum_val = 0
            for j in range(col + 1, n):
                sum_val += rref_matrix[row][j] * vec[j]
            
            # Tính giá trị của biến ở vị trí pivot
            vec[col] = -sum_val / rref_matrix[row][col]
        
        basis.append(vec)
    
    return basis

def compute_inverse(P):
    """Tính ma trận nghịch đảo P^(-1) bằng phương pháp Gauss-Jordan"""
    n = len(P)
    
    # Tạo ma trận mở rộng [P | I]
    P_augmented = []
    for i in range(n):
        row = P[i][:]
        for j in range(n):
            if i == j:
                row.append(1.0)
            else:
                row.append(0.0)
        P_augmented.append(row)
    
    # Biến đổi Gauss-Jordan
    for i in range(n):
        # Tìm pivot
        max_val = abs(P_augmented[i][i])
        max_row = i
        for k in range(i + 1, n):
            if abs(P_augmented[k][i]) > max_val:
                max_val = abs(P_augmented[k][i])
                max_row = k
        
        # Hoán đổi hàng
        if max_row != i:
            P_augmented[i], P_augmented[max_row] = P_augmented[max_row], P_augmented[i]
        
        # Chuẩn hóa hàng pivot
        pivot = P_augmented[i][i]
        for j in range(i, 2*n):
            P_augmented[i][j] /= pivot
        
        # Khử tất cả các hàng khác
        for k in range(n):
            if k != i:
                factor = P_augmented[k][i]
                for j in range(i, 2*n):
                    P_augmented[k][j] -= factor * P_augmented[i][j]
    
    # Trích xuất ma trận nghịch đảo
    P_inverse = []
    for i in range(n):
        P_inverse.append(P_augmented[i][n:])
    
    return P_inverse

def round_matrix(A, decimals=10):
    """Làm tròn các phần tử của ma trận"""
    result = []
    for row in A:
        result.append([round(x, decimals) for x in row])
    return result

def print_matrix(A):
    """In ma trận A"""
    for row in A:
        print([round(x, 10) for x in row])

def is_diagonalizable(A):
    """Kiểm tra ma trận có thể chéo hóa được không và tính ma trận P, P^-1 và D"""
    print("Bước 1: Tính đa thức đặc trưng")
    char_poly = characteristic_polynomial(A)
    print(f"Hệ số của đa thức đặc trưng (theo lũy thừa tăng dần): {char_poly}")
    
    # Kiểm tra tổng các lũy thừa
    n = len(A)
    
    print("\nBước 2: Tìm trị riêng và vector riêng")
    import utils
    # eigenvalues = find_eigenvalues(char_poly)
    eigenvalues = utils.find_eigenvalues(char_poly)
    if sum(eigenvalues.values()) != n:
        print("Ma trận không chéo hóa được: Tổng các lũy thừa khác n")
        return None, None, None
    
    # Tìm vector riêng cho mỗi trị riêng
    eigenvectors = {}
    for eigenval, multiplicity in eigenvalues.items():
        basis = find_eigenvectors(A, eigenval, multiplicity)
        if basis is None:
            print("Ma trận không chéo hóa được: Số chiều không gian nghiệm < bội của trị riêng")
            return None, None, None
        eigenvectors[eigenval] = basis
    
    print("\nBước 3: Xây dựng ma trận P và D")
    # Xây dựng ma trận P từ các vector riêng
    P = create_matrix(n, n)
    D = create_matrix(n, n)
    
    col = 0
    for eigenval, vectors in eigenvectors.items():
        for v in vectors:
            for i in range(n):
                P[i][col] = v[i]
            D[col][col] = eigenval
            col += 1
    
    # Tính P^-1
    P_inverse = compute_inverse(P)
    
    # Kiểm tra P*D*P^-1 = A
    check = matrix_multiply(P, matrix_multiply(D, P_inverse))
    print("\nKiểm tra P*D*P^-1:")
    print_matrix(check)
    
    return P, P_inverse, D

def main():
    # Nhập ma trận đầu vào
    A = [[1, 3, 3], [-3, -5, -3], [3, 3, 1]]

    print("\nMa trận A:")
    print_matrix(A)
    
    P, P_inverse, D = is_diagonalizable(A)
    
    if P is not None:
        print("\nMa trận P (các cột là vector riêng):")
        print_matrix(P)
        
        print("\nMa trận P^-1:")
        print_matrix(P_inverse)
        
        print("\nMa trận đường chéo D:")
        print_matrix(D)
        
        print("\nMa trận A = P*D*P^-1:")
        result = matrix_multiply(P, matrix_multiply(D, P_inverse))
        print_matrix(result)
    else:
        print("\nMa trận không thể chéo hóa được.")

if __name__ == "__main__":
    main()