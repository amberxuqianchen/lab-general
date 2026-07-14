<?php
/**
 * Server Configuration Test Script (PsychoPy / PsychoJS pattern)
 *
 * Based on guilt_expectation_trait_task/test_server_config.php.
 */

echo "<h1>PsychoPy Sample - Server Configuration Test</h1>";
echo "<style>body{font-family:Arial,sans-serif;margin:20px;} .ok{color:green;} .error{color:red;} pre{background:#f0f0f0;padding:10px;}</style>";

echo "<h2>1. PHP Version</h2>";
echo "<p>PHP Version: <strong>" . phpversion() . "</strong></p>";
if (version_compare(phpversion(), '7.0.0', '>=')) {
    echo "<p class='ok'>PHP version is sufficient</p>";
} else {
    echo "<p class='error'>PHP version should be 7.0 or higher</p>";
}

echo "<h2>2. Data Directory</h2>";
$dataDir = __DIR__ . '/data/';
echo "<p>Data directory path: <code>{$dataDir}</code></p>";

if (!file_exists($dataDir)) {
    echo "<p class='error'>Data directory does not exist. Attempting to create...</p>";
    if (mkdir($dataDir, 0755, true)) {
        echo "<p class='ok'>Successfully created data directory</p>";
    } else {
        echo "<p class='error'>Failed to create data directory</p>";
    }
} else {
    echo "<p class='ok'>Data directory exists</p>";
}

echo "<h2>3. Write Permissions</h2>";
if (is_writable($dataDir)) {
    echo "<p class='ok'>Data directory is writable</p>";
} else {
    echo "<p class='error'>Data directory is NOT writable</p>";
    echo "<p>Run: <code>chmod 777 " . htmlspecialchars($dataDir) . "</code></p>";
}

echo "<h2>4. File Writing Test</h2>";
$testFile = $dataDir . 'test_' . date('Y-m-d_His') . '.csv';
$testData = "\xEF\xBB\xBFparticipant,expName\nTEST001,sample_psychopy_task\n";
$result = file_put_contents($testFile, $testData);

if ($result !== false) {
    echo "<p class='ok'>Successfully wrote test file: <code>" . basename($testFile) . "</code></p>";
    if (unlink($testFile)) {
        echo "<p class='ok'>Successfully deleted test file</p>";
    }
} else {
    echo "<p class='error'>Failed to write test file</p>";
}

echo "<h2>5. JSON Support</h2>";
$parsed = json_decode('{"filename":"test.csv","data":"a,b\n1,2"}', true);
if (json_last_error() === JSON_ERROR_NONE) {
    echo "<p class='ok'>JSON parsing works correctly</p>";
} else {
    echo "<p class='error'>JSON parsing failed: " . json_last_error_msg() . "</p>";
}

echo "<h2>6. Existing Data Files</h2>";
if (file_exists($dataDir)) {
    $files = array_diff(scandir($dataDir), ['.', '..', '.htaccess']);
    if (count($files) > 0) {
        echo "<p>Found " . count($files) . " file(s):</p><ul>";
        foreach ($files as $file) {
            $filepath = $dataDir . $file;
            echo "<li><code>{$file}</code> (" . filesize($filepath) . " bytes)</li>";
        }
        echo "</ul>";
    } else {
        echo "<p>No data files yet.</p>";
    }
}

echo "<h2>Summary</h2>";
echo "<p><strong>Next step:</strong> <a href='test_save_data.html'>test_save_data.html</a></p>";
echo "<p>This sample uses the PsychoPy payload shape: <code>{ filename, data }</code>.</p>";
