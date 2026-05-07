SELECT name AS table_name,
       (SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=m.name) AS table_exists
FROM sqlite_master m
WHERE type='table'
ORDER BY name;
