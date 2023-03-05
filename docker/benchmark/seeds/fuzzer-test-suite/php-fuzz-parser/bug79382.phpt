<?php

function strlen(string $x): int {
    $len = 0;
    while (isset($x[$len])) $len++;
    return $len;
}

var_dump(strlen("foobar"));

?>