import pulp

customers = [1, 2, 3, 4, 5]
facilities = ['Fac 1', 'Fac 2', 'Fac 3']
demand = {1 : 80, 2 : 270, 3 : 250, 4 : 160, 5 : 180}
build_cost = {'Fac 1' : 1000, 'Fac 2' : 1000, 'Fac 3' : 1000}
capacity = {'Fac 1' : 500, 'Fac 2' : 500, 'Fac 3' : 500}
shipping_cost = {'Fac 1' : {1 : 4, 2 : 5, 3 : 6, 4 : 8, 5 : 10}, 
                  'Fac 2' : {1 : 6, 2 : 4, 3 : 3, 4 : 5, 5 : 8},
                  'Fac 3' : {1 : 9, 2 : 7, 3 : 4, 4 : 3, 5 : 4}}

model = pulp.LpProblem("CFL", pulp.LpMinimize)

supply = pulp.LpVariable.dicts("Supply", [(i, j) for i in customers
                                                for j in facilities], 0)
                                            
set_fac = pulp.LpVariable.dicts("SetFacility", facilities, 0, 1, pulp.LpBinary)

model += pulp.lpSum(build_cost[j]*set_fac[j] for j in facilities) + \
         pulp.lpSum(shipping_cost[j][i]*supply[(i, j)] for j in facilities for i in customers)

for i in customers:
    model += pulp.lpSum(supply[(i, j)] for j in facilities) == demand[i]

for j in facilities:
    model += pulp.lpSum(supply[(i, j)] for i in customers) <= capacity[j]*set_fac[j]

for i in customers:
    for j in facilities:
        model += supply[(i, j)] <= demand[i]*set_fac[j]


solver = pulp.CPLEX_PY()
solver.buildSolverModel(model)
model.solverModel.parameters.timelimit.set(1800)

start_time = model.solverModel.get_time()
solver.callSolver(model)
end_time = model.solverModel.get_time()


instance_size = len(customers) + len(facilities)
time = end_time - start_time
best_sol = model.solverModel.solution.get_objective_value()
best_bound = model.solverModel.solution.MIP.get_best_objective()
gap = model.solverModel.solution.MIP.get_mip_relative_gap() * 100

print("Tamanho da instancia = %d" % instance_size)
print("Tempo gasto = %f" % time)
print("Melhor solucao = %f" % best_sol)
print("Melhor bound = %f" % best_bound)
print("Gap de otimalidade = %f" % gap)


