SELECT
  test_no,
  model_year,
  make_label AS make,
  model_label AS model,
  body_style,
  crash_type,
  test_config_code,
  test_config_label,
  impact_speed_value,
  impact_speed_unit,
  load_cell_barrier_family,
  load_cell_barrier_classification_id
FROM tests
WHERE test_config_code='VTP'
  AND load_cell_barrier_family='side_pole_load_cell_barrier'
  AND load_cell_barrier_classification_id='side_pole_load_cell_8'
ORDER BY CAST(test_no AS INTEGER);
