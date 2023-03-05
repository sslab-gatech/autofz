<?php
function handleError($level, $message, $file = '', $line = 0, $context = [])
{
    throw new ErrorException($message, 0, $level, $file, $line);
}

set_error_handler('handleError');

$r = new _ZendTestClass;
(string)$r ?: "";

?>