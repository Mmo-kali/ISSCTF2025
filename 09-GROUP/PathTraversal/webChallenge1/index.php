<?php
    // Determine the protocol
    if (!empty($_SERVER['HTTPS']) && ('on' == $_SERVER['HTTPS'])) {
        $uri = 'https://';
    } else {
        $uri = 'http://';
    }
    $uri .= $_SERVER['HTTP_HOST'];

    // Determine the requested path
    $request_uri = $_SERVER['REQUEST_URI'];

    // Redirect based on the requested path
    if ($request_uri == '/contact') {
        header('Location: '.$uri.'/contact.html');
    } elseif ($request_uri == '/about') {
        header('Location: '.$uri.'/about.html');
    }elseif ($request_uri == '/') {
        header('Location: '.$uri.'/index.html');  
    }elseif ($request_uri == '/services') {
        header('Location: '.$uri.'/services.html');
    }
    echo '<p>use this for when the page is broken -> EXAMPLE USAGE: /index.php?page=about.html will include and display the content of about.html</p>';
    $page = $_GET['page']; 
    include('/var/www/webChallenge/' . $page);
	exit;

?>
<DOCTYPE html>
<html>
    <h3> use this for when the page is broken -> EXAMPLE USAGE: /index.php?page=about.html will include and display the content of about.html </h3>
</html> 
