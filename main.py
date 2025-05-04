from col_backtrack_ck import Col_backtrack_ck
from col_fwd_ck import Col_fwd_ck
from col_fwd_mrv_ck import Col_fwd_mrv_ck

solvers = [Col_backtrack_ck, Col_fwd_ck, Col_fwd_mrv_ck]
for solver in solvers:
    curr_solver = solver()
    print(curr_solver.solve(0))
    print(curr_solver)
