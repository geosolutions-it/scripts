DO
$do$
DECLARE
    record RECORD;
    pid_max_time int DEFAULT '5';
    find_slow_query text;
    killing_query text;
BEGIN
    find_slow_query := 'SELECT * FROM pg_stat_activity WHERE 
                        (now() - pg_stat_activity.query_start) > interval $$' || pid_max_time || ' seconds$$ 
                        AND (pg_stat_activity.query ILIKE $$%select max(time)%$$ OR pg_stat_activity.query 
                        ILIKE $$%select min(time)%$$);';
    FOR record IN EXECUTE find_slow_query 
    LOOP
        RAISE NOTICE '-- Found slow query against time field:';
        RAISE NOTICE '%',record.query;
        RAISE NOTICE '-- Gently cancelling slow query with pid: %',record.pid;
        PERFORM pg_cancel_backend(record.pid);
        RAISE NOTICE '-- Then killing the resulting idle slow query';
        PERFORM pg_sleep(0.01);
        PERFORM pg_terminate_backend(record.pid);
        RAISE NOTICE '-- Complete pg_stat_activity row log:';
        RAISE NOTICE '%',record;
    END LOOP;
END
$do$;
