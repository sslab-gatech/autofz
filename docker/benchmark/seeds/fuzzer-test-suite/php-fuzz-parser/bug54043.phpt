<?php

$time = '9999-11-33';	// obviously invalid ;-)
$timeZone = new DateTimeZone('UTC');

try {
    $dateTime = new DateTime($time, $timeZone);
} catch (Exception $e) {
    var_dump($e->getMessage());
}

var_dump(error_get_last());

?>