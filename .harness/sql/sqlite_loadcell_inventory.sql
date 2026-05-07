SELECT
  test_config_code,
  test_config_label,
  load_cell_barrier_family,
  load_cell_barrier_classification_id,
  COUNT(*) AS n_tests
FROM tests
WHERE load_cell_barrier_classification_id IS NOT NULL
GROUP BY
  test_config_code,
  test_config_label,
  load_cell_barrier_family,
  load_cell_barrier_classification_id
ORDER BY n_tests DESC;
