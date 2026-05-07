SELECT
  COALESCE(v.make_label, t.make_label) AS make,
  COALESCE(v.body_style, t.body_style) AS body_style,
  COUNT(*) AS n_vehicle_rows,
  AVG(v.test_weight_kg) AS avg_test_weight_kg,
  AVG(v.curb_weight_kg) AS avg_curb_weight_kg,
  AVG(v.length_mm) AS avg_length_mm,
  AVG(v.width_mm) AS avg_width_mm,
  AVG(v.wheelbase_mm) AS avg_wheelbase_mm,
  AVG(v.vax_crush_distance_mm) AS avg_vax_crush_distance_mm
FROM vehicles v
JOIN tests t ON t.id = v.test_id
WHERE t.test_config_code='VTP'
  AND t.load_cell_barrier_family='side_pole_load_cell_barrier'
  AND t.load_cell_barrier_classification_id='side_pole_load_cell_8'
GROUP BY make, body_style
ORDER BY n_vehicle_rows DESC;
