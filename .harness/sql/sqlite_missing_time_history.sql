SELECT 'files' AS table_name, COUNT(*) AS row_count FROM files
UNION ALL
SELECT 'instrumentation_channels' AS table_name, COUNT(*) AS row_count FROM instrumentation_channels
UNION ALL
SELECT 'injury_metrics' AS table_name, COUNT(*) AS row_count FROM injury_metrics
UNION ALL
SELECT 'intrusions' AS table_name, COUNT(*) AS row_count FROM intrusions;
