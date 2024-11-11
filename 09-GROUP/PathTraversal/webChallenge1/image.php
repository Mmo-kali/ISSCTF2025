<?php
if (isset($_GET['filename'])) {
    $filename = basename($_GET['filename']); // Sanitize the filename
    $filepath = __DIR__ . DIRECTORY_SEPARATOR . 'img' . DIRECTORY_SEPARATOR . $filename; // Adjust the path to your images directory

    if (file_exists($filepath)) {
        $mimeType = mime_content_type($filepath);
        header('Content-Type: ' . $mimeType);
        readfile($filepath);
        exit;
    } else {
        http_response_code(404);
        echo "File not found.";
        exit;
    }
} else {
    http_response_code(400);
    echo "Filename not specified.";
    exit;
}
?>