import numpy as np

step = 0.5

# Var ranges
alpha_range = np.arange(95.0, 130.0 + step, step)
beta_range = np.arange(20.0, 45.0 + step, step)
theta_range = np.arange(10.0, 60.0 + step, step)
l1_range = np.arange(50.0, 150.0 + step, step)
l2_range = np.arange(5000.0, 20000.0 + 10, 10.0)
l3_range = np.arange(50.0, 150.0 + step, step)
l5_range = np.arange(-100.0, 100.0 + step, step)


# Results
best_alpha = 0
best_beta = 0
best_theta = 0
best_l1 = 0
best_l2 = 0
best_l3 = 0
best_l5 = 0

optimal_val = 999999.0
best_LL = 0
best_LR = 0

for alpha in alpha_range:
    for beta in beta_range:
        for theta in theta_range:
            for l1 in l1_range:
                for l2 in l2_range:
                    for l3 in l3_range:
                        for l5 in l5_range:
                            LR = 0  # TODO: FILL THIS SHIT UP
                            LL = 0
                            result = np.abs(LR - LL)

                            if result < optimal_val:
                                print('New optimal: ' + str(result))
                                best_alpha = alpha
                                best_beta = beta
                                best_theta = theta
                                best_l1 = l1
                                best_l2 = l2
                                best_l3 = l3
                                best_l5 = l5

                                optimal_val = result
                                best_LL = LL
                                best_LR = LR

print('\n\n############################')
print('####CALCULATION COMPLETE####')
print('############################')

print('Optimal value: ' + str(optimal_val))
print('Best LL: ' + str(best_LL))
print('Best LR: ' + str(best_LR))
print('Alpha: ' + str(best_alpha))
print('Beta: ' + str(best_beta))
print('Theta: ' + str(best_theta))
print('l1: ' + str(best_l1))
print('l2: ' + str(best_l2))
print('l3: ' + str(best_l3))
print('l5: ' + str(best_l5))
