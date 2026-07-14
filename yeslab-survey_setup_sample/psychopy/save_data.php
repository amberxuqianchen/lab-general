<?php
/**
 * Sample Data Saving Backend (PsychoPy / PsychoJS pattern)
 *
 * Based on guilt_expectation_trait_task/save_data.php.
 * Receives PsychoJS results as a pre-formatted CSV string and writes
 * one file per participant session under data/.
 *
 * Expected request: POST JSON { "filename": "...", "data": "csv string" }
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
define('MAX_FILE_SIZE', 10 * 1024 * 1024);

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

$payload = json_decode($rawInput, true);

if (json_last_error() !== JSON_ERROR_NONE) {
    error_log('JSON decode error: ' . json_last_error_msg());
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Invalid JSON data']);
    exit();
}

if (!is_array($payload)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Payload must be a JSON object']);
    exit();
}

$filename = $payload['filename'] ?? null;
$data = $payload['data'] ?? null;

if (!$filename || !is_string($filename)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Missing filename']);
    exit();
}

if (!preg_match('/^[a-zA-Z0-9_. -]+\.csv$/', $filename)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Invalid filename']);
    exit();
}

if ($data === null || !is_string($data) || $data === '') {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Missing or empty data']);
    exit();
}

$filepath = DATA_DIR . $filename;

$result = file_put_contents($filepath, $data);
if ($result === false) {
    error_log('Failed to write file: ' . $filepath);
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Failed to save data']);
    exit();
}

error_log(sprintf('Successfully saved data to %s (%d bytes)', $filename, $result));

http_response_code(200);
echo json_encode([
    'success' => true,
    'message' => 'Data saved successfully',
    'filename' => $filename,
    'bytes' => $result,
]);
