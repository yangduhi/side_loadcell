# Metric Dictionary

## Loadcell metrics

| Metric | Unit | Definition | Required source |
|---|---|---|---|
| `peak_force_n` | N | Channel or cell maximum force after preprocessing | force-time |
| `time_to_peak_ms` | ms | Time from event zero to peak force | force-time |
| `impulse_n_s` | N·s | Integral of force over analysis window | force-time |
| `force_duration_ms` | ms | Duration where force exceeds project threshold | force-time |
| `force_share` | ratio | Cell/zone force divided by total force at same time | force-time |
| `load_centroid` | mm or normalized | Force-weighted center of load cell layout | force-time + cell layout |

## Vehicle acceleration metrics

| Metric | Unit | Definition | Required source |
|---|---|---|---|
| `peak_accel_mps2` | m/s² | Maximum absolute or signed acceleration per axis policy | acceleration-time |
| `delta_v_mps` | m/s | Integrated acceleration with documented drift correction | acceleration-time |
| `relative_displacement_m` | m | Integrated or externally measured displacement estimate | acceleration-time or displacement channel |

## Energy estimates

| Metric | Unit | Definition | Required source |
|---|---|---|---|
| `cell_energy_j` | J | Integral of cell force over displacement | force-time + displacement estimate |
| `member_energy_j` | J | Weighted cell/zone energy mapped to structural member | energy + mapping matrix |
| `energy_ratio` | ratio | Member or cell energy divided by total estimated energy | energy estimates |
| `specific_energy_j_per_kg` | J/kg | Energy normalized by vehicle test mass | energy + test_weight_kg |
| `crush_normalized_energy_j_per_mm` | J/mm | Energy normalized by crush distance | energy + crush |

All member-level energy values must be labeled `engineering_estimate` and include `confidence`.
