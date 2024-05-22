from pyomo.environ import *
import time
start_time = time.time()
# Tạo mô hình
model = ConcreteModel()

# Tập hợp các nguồn và đích
nguon = ['Nguồn1', 'Nguồn2', 'Nguồn3']
dich = ['Đích1', 'Đích2', 'Đích3']

# Tập hợp các chỉ số
model.N = Set(initialize=nguon)
model.M = Set(initialize=dich)

# Chi phí vận chuyển từng đơn vị hàng hóa từ nguồn đến đích
cost = {
    ('Nguồn1', 'Đích1'): 10,
    ('Nguồn1', 'Đích2'): 20,
    ('Nguồn1', 'Đích3'): 30,
    ('Nguồn2', 'Đích1'): 15,
    ('Nguồn2', 'Đích2'): 25,
    ('Nguồn2', 'Đích3'): 35,
    ('Nguồn3', 'Đích1'): 12,
    ('Nguồn3', 'Đích2'): 22,
    ('Nguồn3', 'Đích3'): 32
}

# Tạo biến số: số lượng hàng hóa được vận chuyển từ mỗi nguồn đến mỗi đích
model.x = Var(model.N, model.M, domain=NonNegativeIntegers)

# Hàm mục tiêu: Tối thiểu hóa chi phí vận chuyển
def objective_rule(model):
    return sum(cost[i, j] * model.x[i, j] for i in model.N for j in model.M)

model.objective = Objective(rule=objective_rule, sense=minimize)

# Ràng buộc: Số lượng hàng hóa cung cấp từ mỗi nguồn không vượt quá lượng hàng hóa có sẵn
def supply_rule(model, i):
    return sum(model.x[i, j] for j in model.M) <= 100  # Giả sử mỗi nguồn cung cấp tối đa 100 đơn vị hàng hóa

model.supply_constraint = Constraint(model.N, rule=supply_rule)

# Ràng buộc: Số lượng hàng hóa cần tại mỗi đích
def demand_rule(model, j):
    return sum(model.x[i, j] for i in model.N) >= 50  # Giả sử mỗi đích cần tối thiểu 50 đơn vị hàng hóa

model.demand_constraint = Constraint(model.M, rule=demand_rule)

# Giải mô hình
solver = SolverFactory('cbc')
solver.solve(model)

# In kết quả
for i in model.N:
    for j in model.M:
        print(f"Số lượng hàng hóa từ {i} đến {j}: {model.x[i, j].value}")
print(f"Chi phí vận chuyển tối thiểu: {model.objective()}")

#in ra thời gian chạy
end_time = time.time()
print(f"Thời gian chạy: {end_time - start_time} giây")