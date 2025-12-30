# HCCDE Deep Validation Battery v2 Summary

## Pass Rates per Condition
> [!NOTE]
> Acceleration is confirmed per-seed if: slope < 0, Cliff's delta < 0, and median late < 0.8 * median early.

| Phase               | Condition                   |   Pass Rate |   N |
|:--------------------|:----------------------------|------------:|----:|
| freeze_constraints  | freeze_constraints          |        0    |  20 |
| parameter_map       | b0.5_l0.01_m0.0             |        0    |   5 |
| parameter_map       | b0.5_l0.01_m0.001           |        0    |   5 |
| parameter_map       | b0.5_l0.01_m0.01            |        0    |   5 |
| parameter_map       | b0.5_l0.01_m0.05            |        0    |   5 |
| parameter_map       | b0.5_l0.05_m0.0             |        0.4  |   5 |
| parameter_map       | b0.5_l0.05_m0.001           |        0    |   5 |
| parameter_map       | b0.5_l0.05_m0.01            |        0    |   5 |
| parameter_map       | b0.5_l0.05_m0.05            |        0    |   5 |
| parameter_map       | b0.5_l0.1_m0.0              |        0.4  |   5 |
| parameter_map       | b0.5_l0.1_m0.001            |        0    |   5 |
| parameter_map       | b0.5_l0.1_m0.01             |        0    |   5 |
| parameter_map       | b0.5_l0.1_m0.05             |        0    |   5 |
| parameter_map       | b1.0_l0.01_m0.0             |        0    |   5 |
| parameter_map       | b1.0_l0.01_m0.001           |        0    |   5 |
| parameter_map       | b1.0_l0.01_m0.01            |        0    |   5 |
| parameter_map       | b1.0_l0.01_m0.05            |        0    |   5 |
| parameter_map       | b1.0_l0.05_m0.0             |        0.6  |   5 |
| parameter_map       | b1.0_l0.05_m0.001           |        0    |   5 |
| parameter_map       | b1.0_l0.05_m0.01            |        0    |   5 |
| parameter_map       | b1.0_l0.05_m0.05            |        0.2  |   5 |
| parameter_map       | b1.0_l0.1_m0.0              |        0.6  |   5 |
| parameter_map       | b1.0_l0.1_m0.001            |        0    |   5 |
| parameter_map       | b1.0_l0.1_m0.01             |        0    |   5 |
| parameter_map       | b1.0_l0.1_m0.05             |        0    |   5 |
| parameter_map       | b1.5_l0.01_m0.0             |        0.4  |   5 |
| parameter_map       | b1.5_l0.01_m0.001           |        0    |   5 |
| parameter_map       | b1.5_l0.01_m0.01            |        0    |   5 |
| parameter_map       | b1.5_l0.01_m0.05            |        0    |   5 |
| parameter_map       | b1.5_l0.05_m0.0             |        1    |   5 |
| parameter_map       | b1.5_l0.05_m0.001           |        0    |   5 |
| parameter_map       | b1.5_l0.05_m0.01            |        0    |   5 |
| parameter_map       | b1.5_l0.05_m0.05            |        0    |   5 |
| parameter_map       | b1.5_l0.1_m0.0              |        1    |   5 |
| parameter_map       | b1.5_l0.1_m0.001            |        0    |   5 |
| parameter_map       | b1.5_l0.1_m0.01             |        0    |   5 |
| parameter_map       | b1.5_l0.1_m0.05             |        0    |   5 |
| power_upgrade       | baseline                    |        0    |  30 |
| power_upgrade       | high_decay                  |        0    |  30 |
| power_upgrade       | no_evolution                |        0    |  30 |
| power_upgrade       | random_evolution            |        0    |  30 |
| target_relocation   | target_relocation           |        0.05 |  20 |
| topology_robustness | erdos_renyi_baseline        |        0    |  20 |
| topology_robustness | erdos_renyi_no_evolution    |        0    |  20 |
| topology_robustness | random_regular_baseline     |        0    |  20 |
| topology_robustness | random_regular_no_evolution |        0    |  20 |
| topology_robustness | small_world_baseline        |        0    |  20 |
| topology_robustness | small_world_no_evolution    |        0    |  20 |

## Robust Metric Averages
| phase               | condition                   |     ht_slope |   acceleration_ratio |   cliffs_delta |
|:--------------------|:----------------------------|-------------:|---------------------:|---------------:|
| freeze_constraints  | freeze_constraints          |  0.020852    |             1.01003  |    -0.007745   |
| parameter_map       | b0.5_l0.01_m0.0             |  0.0238463   |             0.966808 |    -0.00928    |
| parameter_map       | b0.5_l0.01_m0.001           |  0.0224947   |             0.947403 |     0.00416    |
| parameter_map       | b0.5_l0.01_m0.01            |  0.0202524   |             0.931952 |     0.03526    |
| parameter_map       | b0.5_l0.01_m0.05            |  0.0355431   |             0.900416 |     0.04898    |
| parameter_map       | b0.5_l0.05_m0.0             |  0.0052899   |             1.43617  |    -0.0769     |
| parameter_map       | b0.5_l0.05_m0.001           |  0.0221514   |             0.931105 |     0.01492    |
| parameter_map       | b0.5_l0.05_m0.01            |  0.0364787   |             0.829697 |     0.07828    |
| parameter_map       | b0.5_l0.05_m0.05            |  0.0319653   |             1.00676  |     0.01858    |
| parameter_map       | b0.5_l0.1_m0.0              |  0.000232006 |             1.30681  |    -0.09858    |
| parameter_map       | b0.5_l0.1_m0.001            |  0.0275563   |             0.967688 |    -0.0063     |
| parameter_map       | b0.5_l0.1_m0.01             |  0.0256071   |             0.892579 |     0.03078    |
| parameter_map       | b0.5_l0.1_m0.05             |  0.0322339   |             0.961722 |     0.03262    |
| parameter_map       | b1.0_l0.01_m0.0             |  0.0191441   |             1.21205  |    -0.08744    |
| parameter_map       | b1.0_l0.01_m0.001           |  0.061121    |             0.919739 |     0.03498    |
| parameter_map       | b1.0_l0.01_m0.01            |  0.027268    |             1.04298  |    -0.03886    |
| parameter_map       | b1.0_l0.01_m0.05            |  0.0398858   |             1.02089  |    -0.03548    |
| parameter_map       | b1.0_l0.05_m0.0             | -0.00996886  |             1.7154   |    -0.19866    |
| parameter_map       | b1.0_l0.05_m0.001           |  0.0496299   |             0.878113 |     0.05438    |
| parameter_map       | b1.0_l0.05_m0.01            |  0.0377197   |             0.918794 |     0.03658    |
| parameter_map       | b1.0_l0.05_m0.05            |  0.0486265   |             1.02982  |    -0.03856    |
| parameter_map       | b1.0_l0.1_m0.0              | -0.00448431  |             1.60964  |    -0.19868    |
| parameter_map       | b1.0_l0.1_m0.001            |  0.0335413   |             0.965814 |     0.0151     |
| parameter_map       | b1.0_l0.1_m0.01             |  0.0547986   |             0.817582 |     0.0722     |
| parameter_map       | b1.0_l0.1_m0.05             |  0.0378475   |             0.976882 |    -0.03816    |
| parameter_map       | b1.5_l0.01_m0.0             | -0.00245286  |             1.39267  |    -0.16174    |
| parameter_map       | b1.5_l0.01_m0.001           |  0.0703886   |             0.789379 |     0.06908    |
| parameter_map       | b1.5_l0.01_m0.01            |  0.0684409   |             1.09763  |     0.00206    |
| parameter_map       | b1.5_l0.01_m0.05            |  0.0471868   |             1.18752  |    -0.02228    |
| parameter_map       | b1.5_l0.05_m0.0             | -0.0299081   |             2.04753  |    -0.3024     |
| parameter_map       | b1.5_l0.05_m0.001           |  0.0583677   |             1.07024  |    -0.02896    |
| parameter_map       | b1.5_l0.05_m0.01            |  0.0733294   |             1.13906  |    -0.01402    |
| parameter_map       | b1.5_l0.05_m0.05            |  0.0612993   |             1.27171  |    -0.04824    |
| parameter_map       | b1.5_l0.1_m0.0              | -0.0274641   |             2.02061  |    -0.33556    |
| parameter_map       | b1.5_l0.1_m0.001            |  0.0398354   |             1.22782  |    -0.07258    |
| parameter_map       | b1.5_l0.1_m0.01             |  0.0730605   |             1.1151   |     0.0076     |
| parameter_map       | b1.5_l0.1_m0.05             |  0.0635442   |             1.00678  |     0.01026    |
| power_upgrade       | baseline                    |  0.0213005   |             1.0443   |    -0.008695   |
| power_upgrade       | high_decay                  |  0.0285701   |             1.00404  |     0.0080225  |
| power_upgrade       | no_evolution                |  0.0253405   |             1.00861  |     0.008365   |
| power_upgrade       | random_evolution            |  0.0205824   |             1.03175  |    -0.001985   |
| target_relocation   | target_relocation           |  0.0206472   |             0.989302 |     0.00684    |
| topology_robustness | erdos_renyi_baseline        |  0.028742    |             1.01352  |    -0.0106012  |
| topology_robustness | erdos_renyi_no_evolution    |  0.0316867   |             0.973491 |     0.02013    |
| topology_robustness | random_regular_baseline     |  0.0231671   |             1.00515  |    -0.0019225  |
| topology_robustness | random_regular_no_evolution |  0.0245378   |             0.971042 |     0.0158037  |
| topology_robustness | small_world_baseline        |  0.0377933   |             1.04032  |    -0.0025875  |
| topology_robustness | small_world_no_evolution    |  0.0498439   |             1.0714   |    -0.00681875 |

