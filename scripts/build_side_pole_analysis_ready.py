from __future__ import annotations

import csv
import json
import os
import sqlite3
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

DEFAULT_SOURCE_DB = Path(
    r"D:\vscode\nhtsa_metadata\data\refactor_validation_filter_ready_2026-05-07.sqlite"
)
SOURCE_DB = Path(os.getenv("NHTSA_SIDE_LOADCELL_METADATA_DB_PATH", str(DEFAULT_SOURCE_DB)))
FILTERED_TESTS_CSV = DATA / "side_loadcell_filtered_tests.csv"
AVAILABILITY_CSV = DATA / "side_pole_load_cell_channel_availability_2026-05-07.csv"
CHANNEL_NAMES_JSON = DATA / "side_pole_load_cell_and_acceleration_channel_names_2026-05-07.json"

OUTPUT_DB = DATA / "side_pole_analysis_ready_2026-05-07.sqlite"
OUTPUT_JSON = DATA / "side_pole_analysis_ready_2026-05-07.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def clean_axis_key(value: str | None) -> str | None:
    if value is None or value.strip() == "":
        return None
    text = value.strip().lower()
    for old, new in (
        (" - ", "_"),
        (" ", "_"),
        ("-", "_"),
        ("/", "_"),
        ("'", ""),
        ("*", ""),
    ):
        text = text.replace(old, new)
    return "_".join(part for part in text.split("_") if part)


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def optional_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def first_float(*values: Any) -> float | None:
    for value in values:
        parsed = optional_float(value)
        if parsed is not None:
            return parsed
    return None


def first_int(*values: Any) -> int | None:
    parsed = first_float(*values)
    return int(parsed) if parsed is not None else None


def first_text(*values: Any) -> str | None:
    for value in values:
        if value not in (None, ""):
            text = str(value).strip()
            if text:
                return text
    return None


def json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_inputs() -> dict[str, Any]:
    filtered_rows = read_csv(FILTERED_TESTS_CSV)
    availability_rows = read_csv(AVAILABILITY_CSV)
    channel_inventory = json.loads(CHANNEL_NAMES_JSON.read_text(encoding="utf-8"))

    filtered_by_test = {int(row["test_no"]): row for row in filtered_rows}
    availability_by_test = {int(row["test_no"]): row for row in availability_rows}
    json_by_test = {int(row["test_no"]): row for row in channel_inventory["tests"]}

    analysis_test_nos = sorted(
        test_no
        for test_no, row in availability_by_test.items()
        if test_no in filtered_by_test
        and row["test_family"] == "side"
        and row["classification_id"] == "side_pole_load_cell_8"
        and row["family"] == "side_pole_load_cell_barrier"
        and row["normalized_barrier_shape_key"] == "POLE"
    )
    if len(analysis_test_nos) != 554:
        raise RuntimeError(f"Expected 554 analysis tests, got {len(analysis_test_nos)}")

    missing_from_availability = sorted(set(filtered_by_test) - set(availability_by_test))
    if missing_from_availability != [15452]:
        raise RuntimeError(
            "Expected only 15452 to be missing from side-pole availability; "
            f"got {missing_from_availability}"
        )

    for test_no in analysis_test_nos:
        if test_no not in json_by_test:
            raise RuntimeError(f"Analysis test missing from channel JSON: {test_no}")

    return {
        "filtered_rows": filtered_rows,
        "filtered_by_test": filtered_by_test,
        "availability_rows": availability_rows,
        "availability_by_test": availability_by_test,
        "json_by_test": json_by_test,
        "analysis_test_nos": analysis_test_nos,
        "channel_inventory_metadata": channel_inventory["metadata"],
    }


def analysis_grade(row: dict[str, str]) -> tuple[str, bool, bool]:
    strict = bool_text(row["pole_all_1_8_as_measured"]) and bool_text(
        row["vehicle_cg_accel_xyz_as_measured"]
    )
    lateral = bool_text(row["pole_all_1_8_as_measured"]) and bool_text(
        row["vehicle_cg_y_accel_all_as_measured"]
    )
    if strict:
        grade = "strict_full_vector"
    elif lateral:
        grade = "lateral_primary"
    else:
        grade = "inventory_only"
    return grade, strict, lateral


def create_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE analysis_manifest (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE signal_filter_policy (
            policy_id TEXT PRIMARY KEY,
            physical_quantity TEXT NOT NULL,
            default_filter TEXT NOT NULL,
            cfc_class INTEGER,
            preserve_raw_waveform INTEGER NOT NULL,
            applies_to TEXT NOT NULL,
            output_signal TEXT NOT NULL,
            notes TEXT NOT NULL,
            source_basis TEXT NOT NULL
        );

        CREATE TABLE analysis_tests (
            test_no INTEGER PRIMARY KEY,
            test_date TEXT,
            test_type TEXT,
            test_configuration TEXT,
            contractor_study_title TEXT,
            impact_direction TEXT NOT NULL,
            test_family TEXT NOT NULL,
            crash_classification_status TEXT,
            canonical_label TEXT,
            classification_id TEXT NOT NULL,
            family TEXT NOT NULL,
            load_cell_classification_status TEXT NOT NULL,
            raw_barrier_shape TEXT NOT NULL,
            normalized_barrier_shape_key TEXT NOT NULL,
            shape_alias_rule_id TEXT,
            shape_alias_confidence REAL,
            source_scope TEXT NOT NULL
        );

        CREATE TABLE vehicle_specs (
            test_no INTEGER PRIMARY KEY,
            source_vehicle_id INTEGER NOT NULL,
            source_vehicle_no INTEGER,
            participant_kind TEXT NOT NULL,
            participant_kind_source TEXT NOT NULL,
            vin TEXT,
            make TEXT,
            model TEXT,
            model_year INTEGER,
            body_type TEXT,
            engine_type TEXT,
            engine_displacement_l REAL,
            transmission TEXT,
            vehicle_speed_kph REAL,
            vehicle_test_weight_kg REAL,
            curb_weight_kg REAL,
            vehicle_length_mm REAL,
            vehicle_width_mm REAL,
            wheelbase_mm REAL,
            vax_crush_distance_mm REAL,
            vehicle_cg_mm REAL,
            vehicle_orientation_deg REAL,
            source_row_hash TEXT,
            raw_vehicle_json TEXT NOT NULL,
            FOREIGN KEY (test_no) REFERENCES analysis_tests(test_no)
        );

        CREATE TABLE test_qc_summary (
            test_no INTEGER PRIMARY KEY,
            pole_all_1_8_present INTEGER NOT NULL,
            pole_all_1_8_as_measured INTEGER NOT NULL,
            vehicle_cg_accel_xyz_present INTEGER NOT NULL,
            vehicle_cg_accel_xyz_as_measured INTEGER NOT NULL,
            vehicle_cg_accel_any_failed_or_questionable INTEGER NOT NULL,
            strict_full_vector_eligible INTEGER NOT NULL,
            lateral_primary_eligible INTEGER NOT NULL,
            analysis_grade TEXT NOT NULL,
            load_cell_channel_count INTEGER NOT NULL,
            force_channel_count INTEGER NOT NULL,
            moment_channel_count INTEGER NOT NULL,
            vehicle_cg_accel_channel_count INTEGER NOT NULL,
            all_accelerometer_channel_count INTEGER NOT NULL,
            missing_pole_indices TEXT,
            duplicate_pole_indices TEXT,
            vehicle_cg_accel_non_accel_unit_channel_count INTEGER NOT NULL,
            vehicle_cg_accel_non_accel_units TEXT,
            missing_expected_channels_json TEXT NOT NULL,
            duplicate_channels_json TEXT NOT NULL,
            mask_summary_json TEXT NOT NULL,
            FOREIGN KEY (test_no) REFERENCES analysis_tests(test_no)
        );

        CREATE TABLE side_pole_load_cell_channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_no INTEGER NOT NULL,
            instrumentation_channel_id INTEGER,
            curve_no INTEGER NOT NULL,
            qualified_channel_key TEXT NOT NULL,
            pole_index INTEGER,
            derived_channel_name TEXT NOT NULL,
            sensor_type TEXT,
            sensor_location TEXT,
            sensor_attachment TEXT,
            sensor_axis TEXT,
            canonical_axis TEXT,
            axis_key TEXT,
            unit_raw TEXT,
            data_status TEXT,
            channel_status TEXT,
            raw_commentary TEXT,
            channel_role TEXT,
            quantity TEXT,
            is_nominal_pole_index_1_to_8 INTEGER NOT NULL,
            include_in_inventory INTEGER NOT NULL,
            include_in_primary_force_sum INTEGER NOT NULL,
            first_point REAL,
            last_point REAL,
            time_increment REAL,
            raw_fields_json TEXT NOT NULL,
            FOREIGN KEY (test_no) REFERENCES analysis_tests(test_no)
        );

        CREATE TABLE vehicle_cg_acceleration_channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_no INTEGER NOT NULL,
            instrumentation_channel_id INTEGER,
            curve_no INTEGER NOT NULL,
            qualified_channel_key TEXT NOT NULL,
            derived_channel_name TEXT NOT NULL,
            sensor_type TEXT,
            sensor_location TEXT,
            sensor_attachment TEXT,
            sensor_axis TEXT,
            canonical_axis TEXT,
            axis_key TEXT,
            unit_raw TEXT,
            data_status TEXT,
            channel_status TEXT,
            raw_commentary TEXT,
            channel_role TEXT,
            include_in_inventory INTEGER NOT NULL,
            include_in_primary_analysis INTEGER NOT NULL,
            first_point REAL,
            last_point REAL,
            time_increment REAL,
            raw_fields_json TEXT NOT NULL,
            FOREIGN KEY (test_no) REFERENCES analysis_tests(test_no)
        );

        CREATE TABLE download_links (
            id INTEGER PRIMARY KEY,
            test_no INTEGER NOT NULL,
            asset_kind TEXT NOT NULL,
            asset_subtype TEXT,
            source_url TEXT NOT NULL,
            canonical_url_hash TEXT,
            file_ext TEXT,
            suggested_filename TEXT,
            content_type TEXT,
            size_bytes INTEGER,
            title TEXT,
            description TEXT,
            source_payload_id INTEGER,
            source_endpoint_name TEXT,
            source_section_name TEXT,
            source_row_path TEXT,
            source_row_hash TEXT,
            raw_row_json TEXT,
            extra_json TEXT,
            FOREIGN KEY (test_no) REFERENCES analysis_tests(test_no)
        );

        CREATE TABLE download_link_summary (
            test_no INTEGER NOT NULL,
            asset_kind TEXT NOT NULL,
            asset_count INTEGER NOT NULL,
            PRIMARY KEY (test_no, asset_kind),
            FOREIGN KEY (test_no) REFERENCES analysis_tests(test_no)
        );

        CREATE TABLE excluded_tests (
            test_no INTEGER PRIMARY KEY,
            exclusion_reason TEXT NOT NULL,
            source_file TEXT NOT NULL,
            details_json TEXT NOT NULL
        );

        CREATE VIEW waveform_download_links AS
        SELECT *
        FROM download_links
        WHERE asset_kind = 'data_package';

        CREATE VIEW report_download_links AS
        SELECT *
        FROM download_links
        WHERE asset_kind = 'report';

        CREATE VIEW analysis_ready_view AS
        SELECT
            t.test_no,
            t.test_date,
            t.test_type,
            t.test_configuration,
            t.contractor_study_title,
            v.make,
            v.model,
            v.model_year,
            v.body_type,
            v.vehicle_test_weight_kg,
            v.vehicle_length_mm,
            v.vehicle_width_mm,
            v.wheelbase_mm,
            q.analysis_grade,
            q.strict_full_vector_eligible,
            q.lateral_primary_eligible,
            q.force_channel_count,
            q.vehicle_cg_accel_channel_count
        FROM analysis_tests t
        JOIN vehicle_specs v ON v.test_no = t.test_no
        JOIN test_qc_summary q ON q.test_no = t.test_no;

        CREATE INDEX idx_load_cell_channels_test_curve
            ON side_pole_load_cell_channels(test_no, curve_no);
        CREATE INDEX idx_vehicle_cg_channels_test_curve
            ON vehicle_cg_acceleration_channels(test_no, curve_no);
        CREATE INDEX idx_download_links_test_kind
            ON download_links(test_no, asset_kind, asset_subtype);
        CREATE INDEX idx_qc_grade
            ON test_qc_summary(analysis_grade);
        """
    )


def insert_manifest(connection: sqlite3.Connection, inputs: dict[str, Any], generated_at: str) -> None:
    analysis_test_nos = inputs["analysis_test_nos"]
    availability_by_test = inputs["availability_by_test"]
    qc_counts = Counter()
    for test_no in analysis_test_nos:
        grade, strict, lateral = analysis_grade(availability_by_test[test_no])
        qc_counts["strict_full_vector"] += int(strict)
        qc_counts["lateral_primary"] += int(lateral)
        qc_counts[f"grade:{grade}"] += 1

    manifest = {
        "title": "Side pole analysis-ready metadata, channels, vehicle specs, and links",
        "generated_at_utc": generated_at,
        "source_db": str(SOURCE_DB),
        "scope_source": str(FILTERED_TESTS_CSV),
        "availability_source": str(AVAILABILITY_CSV),
        "channel_inventory_source": str(CHANNEL_NAMES_JSON),
        "vehicle_specs_source": str(SOURCE_DB),
        "filtered_test_count": "555",
        "analysis_test_count": str(len(analysis_test_nos)),
        "excluded_filtered_test_count": "1",
        "excluded_research_other_count": "34",
        "waveform_parsed": "false",
        "channel_name_policy": "metadata_derived_not_waveform_native",
        "waveform_binding_key": "test_no+curve_no",
        "strict_full_vector_eligible_count": str(qc_counts["strict_full_vector"]),
        "lateral_primary_eligible_count": str(qc_counts["lateral_primary"]),
    }
    connection.executemany(
        "INSERT INTO analysis_manifest VALUES (?, ?)",
        sorted(manifest.items()),
    )


def insert_filter_policy(connection: sqlite3.Connection) -> None:
    rows = [
        (
            "side_pole_load_cell_individual_force",
            "side pole load-cell individual force",
            "CFC 60",
            60,
            1,
            "per-pole force waveform after test_no+curve_no binding",
            "filtered individual pole force",
            "Apply after waveform timebase reconstruction and baseline handling. Preserve raw waveform separately.",
            "project_filter_policy; SAE J211/NHTSA TP-214P alignment",
        ),
        (
            "side_pole_load_cell_total_force",
            "side pole load-cell total force",
            "CFC 60",
            60,
            1,
            "sum of valid pole force channels",
            "filtered total pole force",
            "Sum only analysis-eligible pole channels unless a partial-force analysis is explicitly requested.",
            "project_filter_policy; SAE J211/NHTSA TP-214P alignment",
        ),
        (
            "vehicle_cg_acceleration",
            "VEHICLE CG acceleration",
            "CFC 60",
            60,
            1,
            "vehicle CG X/Y/Z acceleration channels",
            "filtered vehicle CG acceleration",
            "Keep X/Y/Z axes. Use lateral or impact-axis projection only as a derived signal.",
            "project_filter_policy; SAE J211/NHTSA TP-214P alignment",
        ),
        (
            "acceleration_for_velocity_displacement",
            "velocity/displacement integration acceleration",
            "CFC 180",
            180,
            1,
            "acceleration waveform selected for velocity/displacement integration",
            "integration-ready acceleration",
            "Use for integration workflows; do not replace the CFC 60 acceleration used for force-vs-acceleration comparison.",
            "project_filter_policy; SAE J211/NHTSA TP-214P alignment",
        ),
        (
            "velocity_displacement_result",
            "velocity/displacement result",
            "CFC 180",
            180,
            1,
            "velocity and displacement signals derived from acceleration",
            "filtered velocity/displacement result",
            "Record integration assumptions and source acceleration channel when this signal is generated.",
            "project_filter_policy; SAE J211/NHTSA TP-214P alignment",
        ),
        (
            "raw_waveform",
            "raw waveform",
            "unfiltered",
            None,
            1,
            "all waveform curves downloaded or parsed for this project",
            "raw waveform",
            "Preserve the original unfiltered waveform. Filtered outputs must be additional derived signals.",
            "project_filter_policy",
        ),
    ]
    connection.executemany(
        """
        INSERT INTO signal_filter_policy VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        rows,
    )


def insert_tests(connection: sqlite3.Connection, inputs: dict[str, Any]) -> None:
    rows = []
    for test_no in inputs["analysis_test_nos"]:
        row = inputs["availability_by_test"][test_no]
        rows.append(
            (
                test_no,
                row["test_date"],
                row["test_type"],
                row["test_configuration"],
                row["contractor_study_title"],
                row["impact_direction"],
                row["test_family"],
                row["crash_classification_status"],
                row["canonical_label"] or None,
                row["classification_id"],
                row["family"],
                row["load_cell_classification_status"],
                row["raw_barrier_shape"],
                row["normalized_barrier_shape_key"],
                row["shape_alias_rule_id"],
                float(row["shape_alias_confidence"]),
                "side_loadcell_filtered_tests.csv intersect side_pole_load_cell_8",
            )
        )
    connection.executemany(
        """
        INSERT INTO analysis_tests VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        rows,
    )


def insert_vehicle_specs(connection: sqlite3.Connection, analysis_test_nos: list[int]) -> None:
    source = sqlite3.connect(f"file:{SOURCE_DB.as_posix()}?mode=ro&immutable=1", uri=True)
    source.row_factory = sqlite3.Row
    source.execute("CREATE TEMP TABLE target_test_no(test_no INTEGER PRIMARY KEY)")
    source.executemany("INSERT INTO target_test_no VALUES (?)", [(n,) for n in analysis_test_nos])
    rows = []
    for row in source.execute(
        """
        SELECT
            t.test_no,
            v.id AS source_vehicle_id,
            v.source_vehicle_no,
            p.participant_kind,
            v.make,
            v.model,
            v.model_year,
            v.body_type,
            v.engine_type,
            v.vehicle_speed,
            v.vehicle_test_weight,
            v.curb_weight,
            v.vehicle_length,
            v.vehicle_width,
            v.wheelbase,
            v.vax_crush_distance,
            v.source_row_hash,
            v.raw_row_json
        FROM target_test_no tt
        JOIN tests t ON t.test_no = tt.test_no
        JOIN vehicles v ON v.test_id = t.id
        LEFT JOIN test_participants p ON p.vehicle_id = v.id
        ORDER BY t.test_no
        """
    ):
        raw_vehicle = json.loads(row["raw_row_json"] or "{}")
        explicit_participant = first_text(row["participant_kind"])
        rows.append(
            (
                row["test_no"],
                row["source_vehicle_id"],
                row["source_vehicle_no"],
                explicit_participant or "subject_vehicle",
                "test_participants" if explicit_participant else "single_vehicle_inferred_subject",
                first_text(raw_vehicle.get("VIN")),
                first_text(row["make"], raw_vehicle.get("MAKED")),
                first_text(row["model"], raw_vehicle.get("MODELD")),
                first_int(row["model_year"], raw_vehicle.get("YEAR")),
                first_text(row["body_type"], raw_vehicle.get("BODYD")),
                first_text(row["engine_type"], raw_vehicle.get("ENGINED")),
                first_float(raw_vehicle.get("ENGDSP")),
                first_text(raw_vehicle.get("TRANSMD")),
                first_float(row["vehicle_speed"], raw_vehicle.get("VEHSPD")),
                first_float(row["vehicle_test_weight"], raw_vehicle.get("VEHTWT")),
                first_float(row["curb_weight"], raw_vehicle.get("CURBWT")),
                first_float(row["vehicle_length"], raw_vehicle.get("VEHLEN")),
                first_float(row["vehicle_width"], raw_vehicle.get("VEHWID")),
                first_float(row["wheelbase"], raw_vehicle.get("WHLBAS")),
                first_float(row["vax_crush_distance"]),
                first_float(raw_vehicle.get("VEHCG")),
                first_float(raw_vehicle.get("VEHOR")),
                row["source_row_hash"],
                json_dumps(raw_vehicle),
            )
        )
    source.close()
    if len(rows) != len(analysis_test_nos):
        raise RuntimeError(f"Expected {len(analysis_test_nos)} vehicle rows, got {len(rows)}")
    connection.executemany(
        """
        INSERT INTO vehicle_specs VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        rows,
    )


def insert_qc(connection: sqlite3.Connection, inputs: dict[str, Any]) -> None:
    rows = []
    for test_no in inputs["analysis_test_nos"]:
        row = inputs["availability_by_test"][test_no]
        grade, strict, lateral = analysis_grade(row)
        rows.append(
            (
                test_no,
                int(bool_text(row["pole_all_1_8_present"])),
                int(bool_text(row["pole_all_1_8_as_measured"])),
                int(bool_text(row["vehicle_cg_accel_xyz_present"])),
                int(bool_text(row["vehicle_cg_accel_xyz_as_measured"])),
                int(bool_text(row["vehicle_cg_accel_any_failed_or_questionable"])),
                int(strict),
                int(lateral),
                grade,
                int(row["load_cell_channel_count"]),
                int(row["force_channel_count"]),
                int(row["moment_channel_count"]),
                int(row["vehicle_cg_accel_channel_count"]),
                int(row["all_accelerometer_channel_count"]),
                row["missing_pole_indices"] or None,
                row["duplicate_pole_indices"] or None,
                int(row["vehicle_cg_accel_non_accel_unit_channel_count"]),
                row["vehicle_cg_accel_non_accel_units"] or None,
                row["missing_expected_channels_json"],
                row["duplicate_channels_json"],
                row["mask_summary_json"],
            )
        )
    connection.executemany(
        """
        INSERT INTO test_qc_summary VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        rows,
    )


def raw_float(raw: dict[str, Any], key: str) -> float | None:
    value = raw.get(key)
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def insert_channels(connection: sqlite3.Connection, inputs: dict[str, Any]) -> None:
    load_cell_rows = []
    accel_rows = []
    for test_no in inputs["analysis_test_nos"]:
        availability = inputs["availability_by_test"][test_no]
        inventory = inputs["json_by_test"][test_no]
        for channel in inventory["side_pole_load_cell_channels"]:
            raw_fields = channel.get("raw_fields") or {}
            data_status = channel.get("data_status")
            include_force = (
                bool_text(availability["pole_all_1_8_as_measured"])
                and channel.get("quantity") == "force"
                and channel.get("is_nominal_pole_index_1_to_8") is True
                and data_status == "AS MEASURED"
                and channel.get("channel_status") == "PRIMARY"
            )
            axis_key = clean_axis_key(channel.get("sensor_axis"))
            load_cell_rows.append(
                (
                    test_no,
                    channel.get("instrumentation_channel_id"),
                    int(channel["curve_no"]),
                    channel["qualified_channel_key"],
                    channel.get("pole_index"),
                    channel["derived_channel_name"],
                    channel.get("sensor_type"),
                    channel.get("sensor_location"),
                    channel.get("sensor_attachment"),
                    channel.get("sensor_axis"),
                    channel.get("canonical_axis"),
                    axis_key,
                    channel.get("unit_raw"),
                    data_status,
                    channel.get("channel_status"),
                    channel.get("raw_commentary"),
                    channel.get("channel_role"),
                    channel.get("quantity"),
                    int(channel.get("is_nominal_pole_index_1_to_8") is True),
                    1,
                    int(include_force),
                    raw_float(raw_fields, "NFP"),
                    raw_float(raw_fields, "NLP"),
                    raw_float(raw_fields, "DELT"),
                    json_dumps(raw_fields),
                )
            )
        for channel in inventory["acceleration_channels"]:
            if channel.get("is_vehicle_cg_linear_acceleration") is not True:
                continue
            raw_fields = channel.get("raw_fields") or {}
            axis_key = clean_axis_key(channel.get("sensor_axis"))
            derived_name = f"vehicle_cg.acceleration.{axis_key}" if axis_key else channel[
                "derived_channel_name"
            ]
            include_primary = (
                channel.get("data_status") == "AS MEASURED"
                and channel.get("channel_status") == "PRIMARY"
            )
            accel_rows.append(
                (
                    test_no,
                    channel.get("instrumentation_channel_id"),
                    int(channel["curve_no"]),
                    channel["qualified_channel_key"],
                    derived_name,
                    channel.get("sensor_type"),
                    channel.get("sensor_location"),
                    channel.get("sensor_attachment"),
                    channel.get("sensor_axis"),
                    channel.get("canonical_axis"),
                    axis_key,
                    channel.get("unit_raw"),
                    channel.get("data_status"),
                    channel.get("channel_status"),
                    channel.get("raw_commentary"),
                    channel.get("channel_role"),
                    1,
                    int(include_primary),
                    raw_float(raw_fields, "NFP"),
                    raw_float(raw_fields, "NLP"),
                    raw_float(raw_fields, "DELT"),
                    json_dumps(raw_fields),
                )
            )
    connection.executemany(
        """
        INSERT INTO side_pole_load_cell_channels (
            test_no, instrumentation_channel_id, curve_no, qualified_channel_key,
            pole_index, derived_channel_name, sensor_type, sensor_location,
            sensor_attachment, sensor_axis, canonical_axis, axis_key, unit_raw,
            data_status, channel_status, raw_commentary, channel_role, quantity,
            is_nominal_pole_index_1_to_8, include_in_inventory,
            include_in_primary_force_sum, first_point, last_point, time_increment,
            raw_fields_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        load_cell_rows,
    )
    connection.executemany(
        """
        INSERT INTO vehicle_cg_acceleration_channels (
            test_no, instrumentation_channel_id, curve_no, qualified_channel_key,
            derived_channel_name, sensor_type, sensor_location, sensor_attachment,
            sensor_axis, canonical_axis, axis_key, unit_raw, data_status,
            channel_status, raw_commentary, channel_role, include_in_inventory,
            include_in_primary_analysis, first_point, last_point, time_increment,
            raw_fields_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        accel_rows,
    )


def insert_download_links(connection: sqlite3.Connection, analysis_test_nos: list[int]) -> None:
    source = sqlite3.connect(f"file:{SOURCE_DB.as_posix()}?mode=ro&immutable=1", uri=True)
    source.row_factory = sqlite3.Row
    source.execute("CREATE TEMP TABLE target_test_no(test_no INTEGER PRIMARY KEY)")
    source.executemany("INSERT INTO target_test_no VALUES (?)", [(n,) for n in analysis_test_nos])
    rows = [
        tuple(row)
        for row in source.execute(
            """
            SELECT
                m.id,
                t.test_no,
                m.asset_kind,
                m.asset_subtype,
                m.source_url,
                m.canonical_url_hash,
                m.file_ext,
                m.suggested_filename,
                m.content_type,
                m.size_bytes,
                m.title,
                m.description,
                m.source_payload_id,
                m.source_endpoint_name,
                m.source_section_name,
                m.source_row_path,
                m.source_row_hash,
                m.raw_row_json,
                m.extra_json
            FROM media_assets m
            JOIN tests t ON t.id = m.test_id
            JOIN target_test_no tt ON tt.test_no = t.test_no
            WHERE m.source_url IS NOT NULL
              AND m.source_url != ''
            ORDER BY t.test_no, m.asset_kind, m.asset_subtype, m.id
            """
        )
    ]
    summary_rows = [
        tuple(row)
        for row in source.execute(
            """
            SELECT t.test_no, a.asset_kind, a.asset_count
            FROM asset_summary a
            JOIN tests t ON t.id = a.test_id
            JOIN target_test_no tt ON tt.test_no = t.test_no
            ORDER BY t.test_no, a.asset_kind
            """
        )
    ]
    source.close()
    connection.executemany(
        """
        INSERT INTO download_links VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        rows,
    )
    connection.executemany(
        "INSERT INTO download_link_summary VALUES (?, ?, ?)",
        summary_rows,
    )


def insert_exclusions(connection: sqlite3.Connection, inputs: dict[str, Any]) -> None:
    rows = []
    filtered_by_test = inputs["filtered_by_test"]
    availability_by_test = inputs["availability_by_test"]
    analysis_test_nos = set(inputs["analysis_test_nos"])

    for test_no, row in filtered_by_test.items():
        if test_no not in analysis_test_nos:
            if test_no == 15452:
                reason = "non_side_pole_load_cell_wall_advanced_11x16_176_full"
            else:
                reason = "filtered_scope_not_analysis_ready"
            rows.append((test_no, reason, str(FILTERED_TESTS_CSV), json_dumps(row)))

    for test_no, row in availability_by_test.items():
        if test_no not in filtered_by_test and row.get("test_family") == "research_other":
            rows.append(
                (
                    test_no,
                    "research_other_excluded_by_filtered_scope",
                    str(AVAILABILITY_CSV),
                    json_dumps(row),
                )
            )

    rows = sorted({row[0]: row for row in rows}.values())
    connection.executemany("INSERT INTO excluded_tests VALUES (?, ?, ?, ?)", rows)


def build_json_export(connection: sqlite3.Connection, inputs: dict[str, Any], generated_at: str) -> None:
    connection.row_factory = sqlite3.Row
    metadata = {
        "title": "Side pole analysis-ready export",
        "generated_at_utc": generated_at,
        "source_db": str(SOURCE_DB),
        "scope_source": str(FILTERED_TESTS_CSV),
        "analysis_ready_db": str(OUTPUT_DB),
        "analysis_test_count": 554,
        "excluded_filtered_test_nos": [15452],
        "excluded_research_other_count": 34,
        "side_pole_load_cell_channel_count": 4432,
        "vehicle_cg_acceleration_channel_count": 1662,
        "waveform_parsed": False,
        "channel_name_policy": "metadata_derived_not_waveform_native",
        "waveform_binding_key": ["test_no", "curve_no"],
        "download_links_in_json": "data_package_and_report_only",
        "download_links_full_table": "download_links",
        "filter_policy_table": "signal_filter_policy",
    }

    tests = []
    for row in connection.execute("SELECT * FROM analysis_tests ORDER BY test_no"):
        test = dict(row)
        test_no = test["test_no"]
        vehicle = dict(
            connection.execute(
                """
                SELECT
                    source_vehicle_id, source_vehicle_no, participant_kind,
                    vin, make, model, model_year, body_type, engine_type,
                    engine_displacement_l, transmission, vehicle_speed_kph,
                    vehicle_test_weight_kg, curb_weight_kg, vehicle_length_mm,
                    vehicle_width_mm, wheelbase_mm, vax_crush_distance_mm,
                    vehicle_cg_mm, vehicle_orientation_deg
                FROM vehicle_specs
                WHERE test_no = ?
                """,
                (test_no,),
            ).fetchone()
        )
        qc = dict(
            connection.execute(
                "SELECT * FROM test_qc_summary WHERE test_no = ?",
                (test_no,),
            ).fetchone()
        )
        load_cells = [
            dict(channel)
            for channel in connection.execute(
                """
                SELECT
                    curve_no, pole_index, derived_channel_name, sensor_attachment,
                    sensor_axis, axis_key, unit_raw, data_status, channel_status,
                    raw_commentary, include_in_inventory, include_in_primary_force_sum,
                    first_point, last_point, time_increment
                FROM side_pole_load_cell_channels
                WHERE test_no = ?
                ORDER BY pole_index, curve_no
                """,
                (test_no,),
            )
        ]
        cg_accel = [
            dict(channel)
            for channel in connection.execute(
                """
                SELECT
                    curve_no, derived_channel_name, sensor_attachment, sensor_axis,
                    axis_key, unit_raw, data_status, channel_status, raw_commentary,
                    include_in_inventory, include_in_primary_analysis,
                    first_point, last_point, time_increment
                FROM vehicle_cg_acceleration_channels
                WHERE test_no = ?
                ORDER BY axis_key, curve_no
                """,
                (test_no,),
            )
        ]
        links = [
            dict(link)
            for link in connection.execute(
                """
                SELECT
                    asset_kind, asset_subtype, source_url, file_ext,
                    suggested_filename, title, description
                FROM download_links
                WHERE test_no = ?
                  AND asset_kind IN ('data_package', 'report')
                ORDER BY asset_kind, asset_subtype, suggested_filename
                """,
                (test_no,),
            )
        ]
        tests.append(
            {
                "test": test,
                "vehicle_specs": vehicle,
                "channel_availability_qc": qc,
                "side_pole_load_cell_channels": load_cells,
                "vehicle_cg_acceleration_channels": cg_accel,
                "download_links": links,
            }
        )

    exclusions = [
        dict(row)
        for row in connection.execute(
            "SELECT test_no, exclusion_reason, source_file FROM excluded_tests ORDER BY test_no"
        )
    ]
    filter_policy = [
        dict(row)
        for row in connection.execute(
            "SELECT * FROM signal_filter_policy ORDER BY policy_id"
        )
    ]
    payload = {
        "metadata": metadata,
        "summary": summary_from_db(connection),
        "signal_filter_policy": filter_policy,
        "excluded_tests": exclusions,
        "tests": tests,
    }
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def summary_from_db(connection: sqlite3.Connection) -> dict[str, Any]:
    def scalar(query: str) -> Any:
        return connection.execute(query).fetchone()[0]

    return {
        "analysis_tests": scalar("SELECT COUNT(*) FROM analysis_tests"),
        "vehicle_specs": scalar("SELECT COUNT(*) FROM vehicle_specs"),
        "side_pole_load_cell_channels": scalar("SELECT COUNT(*) FROM side_pole_load_cell_channels"),
        "vehicle_cg_acceleration_channels": scalar(
            "SELECT COUNT(*) FROM vehicle_cg_acceleration_channels"
        ),
        "download_links": scalar("SELECT COUNT(*) FROM download_links"),
        "waveform_download_links": scalar("SELECT COUNT(*) FROM waveform_download_links"),
        "report_download_links": scalar("SELECT COUNT(*) FROM report_download_links"),
        "signal_filter_policy": scalar("SELECT COUNT(*) FROM signal_filter_policy"),
        "excluded_tests": scalar("SELECT COUNT(*) FROM excluded_tests"),
        "strict_full_vector_eligible": scalar(
            "SELECT COUNT(*) FROM test_qc_summary WHERE strict_full_vector_eligible = 1"
        ),
        "lateral_primary_eligible": scalar(
            "SELECT COUNT(*) FROM test_qc_summary WHERE lateral_primary_eligible = 1"
        ),
        "analysis_grade_counts": {
            row["analysis_grade"]: row["n"]
            for row in connection.execute(
                "SELECT analysis_grade, COUNT(*) AS n FROM test_qc_summary GROUP BY analysis_grade"
            )
        },
    }


def validate(connection: sqlite3.Connection) -> None:
    expected = {
        "analysis_tests": 554,
        "vehicle_specs": 554,
        "side_pole_load_cell_channels": 4432,
        "vehicle_cg_acceleration_channels": 1662,
    }
    for table, count in expected.items():
        actual = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        if actual != count:
            raise RuntimeError(f"{table}: expected {count}, got {actual}")
    research_count = connection.execute(
        "SELECT COUNT(*) FROM analysis_tests WHERE test_family != 'side'"
    ).fetchone()[0]
    if research_count != 0:
        raise RuntimeError("analysis_tests contains non-side rows")
    has_15452 = connection.execute(
        "SELECT COUNT(*) FROM analysis_tests WHERE test_no = 15452"
    ).fetchone()[0]
    if has_15452 != 0:
        raise RuntimeError("analysis_tests should not contain 15452")
    strict = connection.execute(
        "SELECT COUNT(*) FROM test_qc_summary WHERE strict_full_vector_eligible = 1"
    ).fetchone()[0]
    lateral = connection.execute(
        "SELECT COUNT(*) FROM test_qc_summary WHERE lateral_primary_eligible = 1"
    ).fetchone()[0]
    if strict != 321 or lateral != 348:
        raise RuntimeError(f"Unexpected analysis subset counts: strict={strict}, lateral={lateral}")
    quick = connection.execute("PRAGMA quick_check").fetchone()[0]
    if quick != "ok":
        raise RuntimeError(f"SQLite quick_check failed: {quick}")


def main() -> None:
    generated_at = utc_now()
    inputs = read_inputs()
    if OUTPUT_DB.exists():
        OUTPUT_DB.unlink()
    connection = sqlite3.connect(OUTPUT_DB)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    create_schema(connection)
    insert_manifest(connection, inputs, generated_at)
    insert_filter_policy(connection)
    insert_tests(connection, inputs)
    insert_vehicle_specs(connection, inputs["analysis_test_nos"])
    insert_qc(connection, inputs)
    insert_channels(connection, inputs)
    insert_download_links(connection, inputs["analysis_test_nos"])
    insert_exclusions(connection, inputs)
    connection.commit()
    validate(connection)
    build_json_export(connection, inputs, generated_at)
    connection.close()

    print(f"created_db={OUTPUT_DB} bytes={OUTPUT_DB.stat().st_size}")
    print(f"created_json={OUTPUT_JSON} bytes={OUTPUT_JSON.stat().st_size}")


if __name__ == "__main__":
    main()
