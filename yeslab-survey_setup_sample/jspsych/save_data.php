<?php
/**
 * Sample Data Saving Backend (jsPsych pattern)
 *
 * Based on congress_semantic/save_data.php.
 * Copy everything in this folder into your experiment root.
 * Receives experiment data as a JSON array of trial objects,
 * validates it, and saves one CSV per participant under data/.
 *
 * Expected request: POST with JSON body = array of trial data rows.
 * Each row should include at least: participant_id
 * Optional but recommended: experiment_version, experiment_start_time
 *
 * Customize $preferredOrder below to match your trial fields.
 */

error_reporting(E_ALL);
ini_set('display_errors', 0);
ini_set('log_errors', 1);
ini_set('error_log', __DIR__ . '/data/error.log');

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit();
}

define('DATA_DIR', __DIR__ . '/data/');
define('MAX_FILE_SIZE', 10 * 1024 * 1024); // 10MB limit

if (!file_exists(DATA_DIR)) {
    if (!mkdir(DATA_DIR, 0755, true)) {
        error_log('Failed to create data directory: ' . DATA_DIR);
        http_response_code(500);
        echo json_encode(['success' => false, 'error' => 'Server configuration error']);
        exit();
    }
}

if (!is_writable(DATA_DIR)) {
    error_log('Data directory is not writable: ' . DATA_DIR);
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Server configuration error']);
    exit();
}

$rawInput = file_get_contents('php://input');

if (empty($rawInput)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'No data received']);
    exit();
}

if (strlen($rawInput) > MAX_FILE_SIZE) {
    http_response_code(413);
    echo json_encode(['success' => false, 'error' => 'Data too large']);
    exit();
}

$data = json_decode($rawInput, true);

if (json_last_error() !== JSON_ERROR_NONE) {
    error_log('JSON decode error: ' . json_last_error_msg());
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Invalid JSON data']);
    exit();
}

if (!is_array($data) || empty($data)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Data must be a non-empty array']);
    exit();
}

$participantID = null;
$experimentVersion = null;
$startTime = null;

foreach ($data as $row) {
    if (isset($row['participant_id'])) {
        $participantID = $row['participant_id'];
    }
    if (isset($row['experiment_version'])) {
        $experimentVersion = $row['experiment_version'];
    }
    if (isset($row['experiment_start_time'])) {
        $startTime = $row['experiment_start_time'];
    }
    if ($participantID && $experimentVersion && $startTime) {
        break;
    }
}

if (!$participantID) {
    error_log('No participant_id found in data');
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Missing participant_id']);
    exit();
}

$safeParticipantID = preg_replace('/[^a-zA-Z0-9_-]/', '_', $participantID);

$timestamp = date('Y-m-d_His');
$filename = sprintf(
    'participant_%s_%s_v%s.csv',
    $safeParticipantID,
    $timestamp,
    $experimentVersion ?? 'unknown'
);
$filepath = DATA_DIR . $filename;

$allHeaders = [];
foreach ($data as $row) {
    $allHeaders = array_merge($allHeaders, array_keys($row));
}
$allHeaders = array_unique($allHeaders);

// Customize this list for your experiment columns
$preferredOrder = [
    'participant_id',
    'experiment_version',
    'experiment_start_time',
    'sona_survey_code',
    'task',
    'block',
    'stimulus_name',
    'response',
    'rt',
    'time_elapsed',
    'trial_index',
    'trial_type'
];

$orderedHeaders = [];
foreach ($preferredOrder as $header) {
    if (in_array($header, $allHeaders)) {
        $orderedHeaders[] = $header;
    }
}
foreach ($allHeaders as $header) {
    if (!in_array($header, $orderedHeaders)) {
        $orderedHeaders[] = $header;
    }
}

$file = fopen($filepath, 'w');
if ($file === false) {
    error_log('Failed to open file for writing: ' . $filepath);
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Failed to save data']);
    exit();
}

fputcsv($file, $orderedHeaders);

foreach ($data as $row) {
    $orderedRow = [];
    foreach ($orderedHeaders as $header) {
        $orderedRow[] = isset($row[$header]) ? $row[$header] : '';
    }
    fputcsv($file, $orderedRow);
}

fclose($file);

error_log(sprintf(
    'Successfully saved data for participant %s (%d rows) to %s',
    $participantID,
    count($data),
    $filename
));

http_response_code(200);
echo json_encode([
    'success' => true,
    'message' => 'Data saved successfully',
    'filename' => $filename,
    'rows' => count($data)
]);
